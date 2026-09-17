# Bibliotecas C++ externas

O conteúdo de `third_party/` é fonte externa vendorizada. Ele não deve ser
ligado diretamente pelos aplicativos Kotlin.

Quando uma biblioteca externa precisar participar do aplicativo:

1. uma receita Conan deve descrevê-la;
2. Conan deve produzir o pacote binário para a ABI Android;
3. CMake deve consumir o pacote gerado;
4. Djinni deve expor somente a API necessária ao Kotlin.

