# Boden Logger

Logger C++ baseado no módulo `logger` de `nativium-modules`, sem Djinni ou
serviços escritos em Java/Objective-C.

O pacote Conan `boden-logger/0.1.0` fornece o alvo CMake
`boden::logger`. Ele depende de `boden-datetime` para incluir horário nas
mensagens.

Os níveis são `Verbose`, `Debug`, `Info`, `Warning` e `Error`.
O `StreamLogSink` escreve no console, enquanto aplicações podem instalar
outro `LogSink`, por exemplo para mostrar o histórico em um componente Yoga.
