# Substance Connector

Substance Connector is a communication framework for connecting applications
to share generic data. Our initial use case is to automate and
simplify the process of exporting and importing assets between applications. 
This framework can be expanded for use in sharing any data between applications.

## CLI Tools and Default Build

The default CMake project build will create the Python project folder for
the CLI tool set. The CLI tools act as a connector endpoint and can be used
to test features and/or integrations of Substance Connector. The CLI tools also
acts as a recommended example of how a connector integration is structured.
The CLI tools are written in Python but the structure remains the same for all
language implementations. The default install directory will either be
`./install` or `./cli/install` based on if CMake is run at the root or within the
`./cli` folder respectively.

## Implementation Details

The core library is implemented in C for easier FFI.


### Using the Framework

Build flags are listed in the top level of the [CMake file](./CMakeLists.txt).
Using separate builds per language binding is recommended to avoid conflict errors.
Enabling the QT module flag will build core, C++ module, and the QT module. 

When no flags are set, the project will default to building the CLI tools.

The general lifecycle of an integration is as follows:
- Create instance
- Create feature components
- Bind callbacks to components
- Initialize instance
- Broadcast that a new instance is available
- Shutdown

Connections are automatic once a broadcast message has been sent. 
Every existing connector endpoint will have the context of a new connection and vice versa. 

### Expanding the Framework 

Messages are sent as a JSON formatted string.
The [`application.h`](./module-cpp/include/substance/connector/framework/application.h) file in the C++ module is the base for feature components.
The [`export.h`](./module-cpp/include/substance/connector/framework/export.h) is an implementation of a feature. 
In this instance, we are creating a feature component that handles the sending and receiving of assets without additional context for exporting and importing. 

*For adding a PR of a new feature/schema, json is expected and an implementation is expected in all language modules.*


### Coding Style

The naming convention for functions is as follows:
    * All externally facing functions shall be prefixed by substance_connector
    * All internal functions that do not have static linkage are prefixed
      by connector (code inside the details folder)
    * All static functions need not be prefixed by either

Some **internal headers** have compatibility with C++, to leverage C++ testing engines with the internals of the libraries. 
This isn't a requirement but may be needed for testing to ensure proper linking.

All **external headers** must be wrapped in extern "C" declarations for C++ compatibility with a corresponding test for C++ defines so that they may also be used in C.

**Headers** must have a guard statement with the format `_SUBSTANCE_CONNECTOR_<HEADER>_H` to ensure reasonable header define namespacing.

**External headers** should be located in the `include/substance/connector` folder, meaning that with include as an include directory, an application can include a header with `#include <substance/connector/<header>.h>`. 

All **headers** used internally must be in the details subfolder to be included as `#include <substance/connector/details/<header>.h>` by any internal file or the testing suite.

All **macro flags** are to be respected at compile time (wrapped in ifndef flags) and must be prefixed with `SUBSTANCE_CONNECTOR`. 
Flags shared between files, such as in a header, must use the same prefix. 

Macros used within a single file should be prefixed with `CONNECTOR`.
**Enum constants** shall also use the `SUBSTANCE_CONNECTOR` prefix, and be in all caps,
Enums scoped to a compilation unit, such as inside a .c file, should be prefixed by `CONNECTOR` and remain in all caps.
**Typedefs** for structure types or enum types should have the format `connector_<name>_t` if internal and `substance_connector_<name>_t` if external
**Function pointers** will have the same convention, except with `_fp` at the end instead of `_t`.
**Structs** generally have the form `struct _connector_<name>`, with the corresponding typedef as `connector_<name>_t`.
**Snake case** should be used for variable names and function names.
**Allman-style braces** should be used, with four spaces for indentation.

**Variables** should always have an initial value, unless some form of struct.
**Pointers**:
  - must be initialized to a value or `NULL`. 
  - should be declared constant if they are not modified unless the
internal function reserves the right to modify it.

**Integers** should be initialized to an intentional value or zero.
**Memory allocations** must go through the proper `connector_allocate` and `connector_free` calls to ensure a standard memory allocation throughout the codebase.
The API allows for changing the allocator and free function before initialization.

### Compile flags 

- `SUBSTANCE_CONNECTOR_CONTEXT_COUNT`: The context count.
- `SUBSTANCE_CONNECTOR_FORCE_SELECT` & `SUBSTANCE_CONNECTOR_FORCE_POLL`: the update method (?), if both are specified SELECT will be used.    
- `SUBSTANCE_CONNECTOR_INBOUND_COUNT`: Inbound thread count
- `SUBSTANCE_CONNECTOR_OUTBOUND_COUNT`: Outbound thread count
- `SUBSTANCE_CONNECTOR_DISPATCH_COUNT`: The number of dispatch threads
- `SUBSTANCE_CONNECTOR_SOCK_BACKLOG`: Number of connections to allow on a listen call

### Bindings

**Currently supported language bindings**:
- C, C++ (Natively)
- Python 2
- Python 3
- Tcl
- Haskell
- Qml
- SBCL Common Lisp

**Tested build platforms (just C)**:
- Linux (x86-64, arm-musl-32-bit, arm-musl-64-bit, PowerPC 32-bit)
- MacOS (x86-64)
