from kivy.properties import (
    BooleanProperty, StringProperty, NumericProperty, ListProperty
    )
from kivent_core.rendering.vertex_formats cimport (
    VertexFormat4F, VertexFormat2F4UB, VertexFormat7F, VertexFormat4F4UB,
    VertexFormat7F4UB
    )
from kivent_core.rendering.vertex_formats import (
    vertex_format_4f, vertex_format_7f, vertex_format_4f4ub, 
    vertex_format_2f4ub, vertex_format_7f4ub
    )
from kivent_core.rendering.cmesh cimport CMesh
from kivent_core.rendering.vertex_format cimport KEVertexFormat
from kivent_core.rendering.batching cimport BatchManager, IndexedBatch
from kivy.graphics.cgl cimport GLfloat, GLushort


# cython: embedsignature=True
from kivent_core.systems.staticmemgamesystem cimport StaticMemGameSystem, MemComponent, ComponentPointerAggregator
from kivent_core.memory_handlers.block cimport MemoryBlock
from kivent_core.memory_handlers.indexing cimport IndexedMemoryZone
from kivent_core.memory_handlers.membuffer cimport Buffer
from kivent_core.memory_handlers.zone cimport MemoryZone
from kivent_core.rendering.model cimport VertexModel
from kivent_core.systems.renderers cimport Renderer

from kivy.factory import Factory
from kivy.properties import ObjectProperty, NumericProperty, StringProperty


cdef class ParallaxComponent2D(MemComponent):
    '''The component associated with ParallaxSystem2D.

    **Attributes:**
        **entity_id** (unsigned int): The entity_id this component is currently
        associated with. Will be <unsigned int>-1 if the component is
        unattached.

        **shift** (float): How much to shift the object.
    '''

    property entity_id:
        def __get__(self):
            cdef ParallaxStruct2D* data = <ParallaxStruct2D*>self.pointer
            return data.entity_id

    property shift:
        def __get__(self):
            cdef ParallaxStruct2D* data = <ParallaxStruct2D*>self.pointer
            return data.shift
        def __set__(self, float value):
            cdef ParallaxStruct2D* data = <ParallaxStruct2D*>self.pointer
            data.shift = value


cdef class ParallaxSystem2D(StaticMemGameSystem):
    '''
    ParallaxSystem2D abstracts 2 dimensional rotation data out into its own
    system so that all other GameSystem can interact with the rotation of an
    Entity without having to know specifically about dependent systems such as
    the CymunkPhysics system or any other method of determining the actual
    rotation. This GameSystem does no processing of its own, just holding data.

    Typically other GameSystems will interpret this rotation as being a
    rotation around the center of the entity.
    '''
    type_size = NumericProperty(sizeof(ParallaxStruct2D))
    component_type = ObjectProperty(ParallaxComponent2D)
    system_id = StringProperty('parallax_renderer')

    def init_component(self, unsigned int component_index,
        unsigned int entity_id, str zone, args):
        '''A ParallaxComponent2D is always initialized with a single float
        representing a rotation in degrees.
        '''
        cdef MemoryZone memory_zone = self.imz_components.memory_zone
        cdef ParallaxStruct2D* component = <ParallaxStruct2D*>(
            memory_zone.get_pointer(component_index))
        component.entity_id = entity_id
        component.shift = args['shift']

    def clear_component(self, unsigned int component_index):
        cdef MemoryZone memory_zone = self.imz_components.memory_zone
        cdef ParallaxStruct2D* pointer = <ParallaxStruct2D*>(
            memory_zone.get_pointer(component_index))
        pointer.entity_id = -1
        pointer.shift = 1.0


cdef class ParallaxRenderer(Renderer):

    system_id = StringProperty('parallax_renderer')
    system_names = ListProperty(['parallax_renderer', 'position', ])
    model_format = StringProperty('vertex_format_4f')
    vertex_format_size = NumericProperty(sizeof(VertexFormat4F))

    cdef void* setup_batch_manager(self, Buffer master_buffer) except NULL:
        '''
        Function called internally during **allocate** to setup the
        BatchManager. The KEVertexFormat should be initialized in this
        function as well.
        '''
        cdef KEVertexFormat batch_vertex_format = KEVertexFormat(
            sizeof(VertexFormat4F), *vertex_format_4f)
        self.batch_manager = BatchManager(
            self.size_of_batches, self.max_batches, self.frame_count,
            batch_vertex_format, master_buffer, 'triangles', self.canvas,
            [x for x in self.system_names],
            self.smallest_vertex_count, self.gameworld)
        return <void*>self.batch_manager

    def update(self, force_update, dt):
        '''
        Update function where all drawing of entities is performed.
        Override this method if you would like to create a renderer with
        customized behavior. The basic logic is that we iterate through
        each batch getting the entities in that batch, then iterate through
        the vertices in the RenderComponent.vert_mesh, copying every
        vertex into the batches data and combining it with data from other
        components.
        Args:
            dt (float): The time elapsed since last update, not usually
            used in rendering but passed in to maintain a consistent API.
        '''
        cdef IndexedBatch batch
        cdef list batches
        cdef unsigned int batch_key
        cdef unsigned int index_offset, vert_offset
        cdef RenderStruct* render_comp
        cdef PositionStruct2D* pos_comp
        cdef ParallaxStruct2D* par_comp
        cdef VertexFormat4F* frame_data
        cdef GLushort* frame_indices
        cdef VertexFormat4F* vertex
        cdef VertexModel model
        cdef GLushort* model_indices
        cdef VertexFormat4F* model_vertices
        cdef VertexFormat4F model_vertex
        cdef unsigned int used, i, ri, component_count, n, t
        cdef ComponentPointerAggregator entity_components
        cdef BatchManager batch_manager = self.batch_manager
        cdef dict batch_groups = batch_manager.batch_groups
        cdef CMesh mesh_instruction
        cdef MemoryBlock components_block
        cdef void** component_data
        cdef bint static_rendering = self.static_rendering

        for batch_key in batch_groups:
            batches = batch_groups[batch_key]
            for batch in batches:
                if not static_rendering or force_update:
                    entity_components = batch.entity_components
                    components_block = entity_components.memory_block
                    used = components_block.used_count
                    component_count = entity_components.count
                    component_data = <void**>components_block.data
                    frame_data = <VertexFormat4F*>batch.get_vbo_frame_to_draw()
                    frame_indices = <GLushort*>batch.get_indices_frame_to_draw()
                    index_offset = 0
                    for t in range(used):
                        ri = t * component_count
                        if component_data[ri] == NULL:
                            continue
                        render_comp = <RenderStruct*>component_data[ri+0]
                        vert_offset = render_comp.vert_index
                        model = <VertexModel>render_comp.model
                        if render_comp.render:

                            pos_comp = <PositionStruct2D*>component_data[ri+1]

                            model_vertices = <VertexFormat4F*>(
                                model.vertices_block.data)
                            model_indices = <GLushort*>model.indices_block.data
                            for i in range(model._index_count):
                                frame_indices[i+index_offset] = (
                                    model_indices[i] + vert_offset)
                            for n in range(model._vertex_count):
                                vertex = &frame_data[n + vert_offset]
                                model_vertex = model_vertices[n]
                                vertex.pos[0] = pos_comp.x + pos_comp.shift + model_vertex.pos[0]
                                vertex.pos[1] = pos_comp.y + model_vertex.pos[1]
                                vertex.uvs[0] = model_vertex.uvs[0]
                                vertex.uvs[1] = model_vertex.uvs[1]
                            index_offset += model._index_count
                    batch.set_index_count_for_frame(index_offset)
                mesh_instruction = batch.mesh_instruction
                mesh_instruction.flag_update()

Factory.register('ParallaxSystem2D', cls=ParallaxSystem2D)
Factory.register('ParallaxRenderer', cls=ParallaxRenderer)
