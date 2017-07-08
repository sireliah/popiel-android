from kivent_core.systems.staticmemgamesystem cimport StaticMemGameSystem, MemComponent

ctypedef struct RenderStruct:
    unsigned int entity_id
    unsigned int texkey
    unsigned int batch_id
    void* model
    void* renderer
    int vert_index
    int ind_index
    bint render

ctypedef struct PositionStruct2D:
    unsigned int entity_id
    float x
    float y
    float shift

ctypedef struct ParallaxStruct2D:
    unsigned int entity_id
    float shift


cdef class ParallaxComponent2D(MemComponent):
    pass


cdef class ParallaxSystem2D(StaticMemGameSystem):
    pass
