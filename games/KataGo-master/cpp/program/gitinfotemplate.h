#define STRINGIFY_GIT_REV(x) #x
#define STRINGIFY_GIT_REV2(x) STRINGIFY_GIT_REV(x)
#define GIT_REVISION STRINGIFY_GIT_REV2(GIT_REVISION_)
#define GIT_REVISION_ \
