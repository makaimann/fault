import pathlib
import tempfile
import fault
import magma as m
import os


def test_include_verilog():
    SB_DFF = m.DeclareCircuit('SB_DFF', "D", m.In(m.Bit), "Q", m.Out(m.Bit),
                              "C", m.In(m.Clock))
    main = m.DefineCircuit('main', "I", m.In(m.Bit), "O", m.Out(m.Bit),
                           *m.ClockInterface())
    ff = SB_DFF()
    m.wire(ff.D, main.I)
    m.wire(ff.Q, main.O)
    m.EndDefine()

    tester = fault.Tester(main, main.CLK)
    tester.poke(main.I, 1)
    tester.eval()
    tester.expect(main.O, 0)
    tester.step(2)
    tester.expect(main.O, 1)
    sb_dff_filename = pathlib.Path("tests/sb_dff_sim.v").resolve()
    with tempfile.TemporaryDirectory() as tmp_dir:
        tester.compile_and_run(target="verilator", directory=tmp_dir,
                               include_verilog_libraries=[sb_dff_filename])

    # Should work by including the tests/ directory which contains the verilog
    # file SB_DFF.v
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with tempfile.TemporaryDirectory() as tmp_dir:
        tester.compile_and_run(target="verilator", directory=tmp_dir,
                               include_directories=[dir_path])