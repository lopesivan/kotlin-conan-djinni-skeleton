# Boden String Helper

Camada C++ reutilizável extraída conceitualmente do módulo `string-helper` de
`nativium-modules`. Esta versão não depende de Djinni, Java, Objective-C ou
WebAssembly.

A API pública fica em `bdn/modules/StringHelper.h` e oferece trim, conversão
de caixa, separação de texto e codificação/decodificação de componentes URI.
O módulo é consumido pelos aplicativos por meio do pacote Conan
`boden-string/0.1.0` e do alvo CMake `boden::string`.
