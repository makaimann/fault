from fault import PythonTester
from ..common import AndCircuit, SimpleALU
from hwtypes import BitVector


def test_interactive_basic(capsys):
    tester = PythonTester(AndCircuit)
    tester.poke(AndCircuit.I0, 0)
    tester.poke(AndCircuit.I1, 1)
    tester.eval()
    tester.expect(AndCircuit.O, 0)
    tester.poke(AndCircuit.I0, 1)
    tester.eval()
    tester.assert_(tester.peek(AndCircuit.O) == 1)
    tester.print("Hello %d\n", AndCircuit.O)
    assert capsys.readouterr()[0] == "Hello 1\n"


def test_interactive_setattr():
    tester = PythonTester(AndCircuit)
    tester.circuit.I0 = 1
    tester.circuit.I1 = 1
    tester.eval()
    tester.circuit.O.expect(1)


def test_interactive_clock():
    tester = PythonTester(SimpleALU, SimpleALU.CLK)
    tester.circuit.a = 0xDEAD
    tester.circuit.b = 0xBEEF
    tester.circuit.CLK = 0
    tester.circuit.config_data = 1
    tester.circuit.config_en = 1
    tester.step(2)
    tester.circuit.c.expect(BitVector[16](0xDEAD) - BitVector[16](0xBEEF))
