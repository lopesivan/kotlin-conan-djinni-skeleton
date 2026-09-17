# Boden File Helper

Camada C++20 baseada no módulo `file-helper` de `nativium-modules`.
Ela usa `std::filesystem` e fluxos padrão, sem Poco, Djinni, Java ou
Objective-C.

O pacote Conan é `boden-file-helper/0.1.0`, exposto ao CMake como
`boden::file-helper`. A API inclui texto, bytes, diretórios, listagem,
cópia, movimentação, remoção e consultas de caminho.

As funções de entrada e saída lançam exceções em caso de falha, evitando a
ambiguidade entre arquivo vazio e erro de leitura.
