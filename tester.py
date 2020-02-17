from parser import parse_instructions, get_functions
from cf_graph import CFGraph
from ir_generation import generate_ir



def test_quicksort():
    instructions = parse_instructions("public_test_cases/quicksort/quicksort.ir")
    functions = get_functions(instructions)
    cfgs = [CFGraph.build(func) for func in functions]
    for cfg in cfgs:
        cfg.display()
    generate_ir(instructions, "quicksort.ir")

def main():
    test_quicksort()


if __name__ == '__main__':
    main()