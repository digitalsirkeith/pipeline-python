from dotenv import load_dotenv
load_dotenv()
from library.genetic import Population, Sample

pop = Population()

for idx,sample in enumerate(pop.samples):
    sample.set_score(10-idx)

for idx,sample in enumerate(pop.samples):
    print(idx,sample)

print('')
for i in range(10):
    pop.generate_next()
    for idx,sample in enumerate(pop.samples):
        print(idx,sample)   
    print('')