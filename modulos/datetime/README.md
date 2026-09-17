# Boden DateTime

Camada C++ reutilizável baseada no módulo `datetime` de
`nativium-modules`, sem Djinni, Java, Objective-C ou WebAssembly.

A API pública fica em `bdn/modules/DateTime.h`. Ela oferece obtenção do
relógio atual, parsing e formatação, timestamps em segundos e milissegundos e
conversão de textos de horário.

O pacote Conan é `boden-datetime/0.1.0`, exposto ao CMake como
`boden::datetime`. A implementação usa `date/3.0.4` em modo header-only.

A conversão por fuso POSIX do módulo original não faz parte da versão 0.1.0,
pois dependia de `date/ptz.h`, uma extensão específica daquela árvore.
