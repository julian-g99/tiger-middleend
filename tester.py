from parser import parse_instructions, get_functions
from cf_graph import CFGraph
from ir_generation import generate_ir
from optimizer import deadcode_elim_marksweep



def test_quicksort():
    instructions = parse_instructions("public_test_cases/quicksort/quicksort.ir")
    functions = get_functions(instructions)
    cfgs = [CFGraph.build(func) for func in functions]
    optimized_instructions = []
    for cfg in cfgs:
        deadcode_elim_marksweep(cfg)
        optimized_instructions += cfg.instructions
    generate_ir(optimized_instructions, "quicksort.ir")

def main():
    test_quicksort()


if __name__ == '__main__':
    main()
