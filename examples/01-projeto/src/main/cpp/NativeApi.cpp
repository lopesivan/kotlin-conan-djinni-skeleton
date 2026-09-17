#include "native_api.hpp"

#include <string>

std::string generated::NativeApi::hello_from_cpp()
{
    return "Hello from C++ via Djinni";
}
