from hvc_neural_data_generator import DataGenerator, GeneratorConfig

cfg = GeneratorConfig(
    time=500,
    dim=247,
    RAdim=495,
    nbr_gaps=20,
    alpha=0.5,
)

gen = DataGenerator(cfg, seed=42)
gen.run_and_save(outdir="results")
