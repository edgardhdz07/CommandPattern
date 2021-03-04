from __future__ import annotations
from abc import ABC, abstractmethod

class Command(ABC):
    #La interfaz Command declara un método para ejecutar un comando

    @abstractmethod
    def execute(self) -> None:
        pass

class SimpleCommand(Command):
    #Algunos comandos pueden implementar operaciones simples por sí mismos.

    def __init__(self, payload: str) -> None:
        self._payload = payload

    def execute(self) -> None:
        print(f"SimpleCommand: See, I can do simple things like printing"
              f"({self._payload})")

class ComplexCommand(Command):
    #Sin embargo, algunos comandos pueden delegar operaciones más complejas en otros objetos, llamados "receptores".

    def __init__(self, receiver: Receiver, a: str, b: str) -> None:
        #Los comandos complejos pueden aceptar uno o varios objetos receptores junto con cualquier dato de contexto a través del constructor.

        self._receiver = receiver
        self._a = a
        self._b = b

    def execute(self) -> None:
        #Los comandos pueden delegar en cualquier método de un receptor.

        print("ComplexCommand: Complex stuff should be done by a receiver object", end="")
        self._receiver.do_something(self._a)
        self._receiver.do_something_else(self._b)

class Receiver:
    '''
    Las clases receptoras contienen una importante lógica de negocio. 
    Saben cómo realizar todo tipo de operaciones, asociadas a la realización de una solicitud. 
    De hecho, cualquier clase puede servir como receptor.
    '''
    def do_something(self, a: str) -> None:
        print(f"\nReceiver: Working on ({a}.)", end="")

    def do_something_else(self, b: str) -> None:
        print(f"\nReceiver: Also working on ({b}.)", end="")

class Invoker:
    #El Invoker está asociado a uno o varios comandos. Envía una solicitud al comando.

    _on_start = None
    _on_finish = None

    #Inicializa los comandos.

    def set_on_start(self, command: Command):
        self._on_start = command

    def set_on_finish(self, command: Command):
        self._on_finish = command

    def do_something_important(self) -> None:
        '''
        El Invoker no depende de clases concretas de comando o receptor. 
        El Invoker pasa una petición a un receptor indirectamente, ejecutando un comando.
        '''

        print("Invoker: Does anybody want something done before I begin?")
        if isinstance(self._on_start, Command):
            self._on_start.execute()

        print("Invoker: ...doing something really important...")

        print("Invoker: Does anybody want something done after I finish?")
        if isinstance(self._on_finish, Command):
            self._on_finish.execute()

if __name__ == "__main__":
    #El código del cliente puede parametrizar un invocador con cualquier comando.

    invoker = Invoker()
    invoker.set_on_start(SimpleCommand("Say Hi!"))
    receiver = Receiver()
    invoker.set_on_finish(ComplexCommand(
        receiver, "Send email", "Save report"))

    invoker.do_something_important()
