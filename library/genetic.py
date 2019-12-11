import os, random

class Sample():
    def __init__(self, compression_level, ce_bufsize, et_bufsize, block_size):
        self.compression_level = compression_level
        self.ce_bufsize = ce_bufsize
        self.et_bufsize = et_bufsize
        self.block_size = block_size
        self.score = 0

    def __repr__(self):
        return f'{self.compression_level}-{self.ce_bufsize}-{self.et_bufsize}-{self.block_size}-{self.score}'

    def mutate(self):
        compression_level = (self.compression_level + random.randint(-4, 4)) % 10
        ce_bufsize = 2 + ((self.ce_bufsize + random.randint(-10, 6)) % 32)
        et_bufsize = 2 + ((self.et_bufsize + random.randint(-10, 6)) % 32)
        block_size = 32 + ((self.block_size + random.randint(-8192, 8192)) % 16352)

        return Sample(compression_level, ce_bufsize, et_bufsize, block_size)

    def crossover(self, other):
        compression_level = self.compression_level if random.random() > 0.5 else other.compression_level
        ce_bufsize = self.ce_bufsize if random.random() > 0.5 else other.ce_bufsize
        et_bufsize = self.et_bufsize if random.random() > 0.5 else other.et_bufsize
        block_size = self.block_size if random.random() > 0.5 else other.block_size

        return Sample(compression_level, ce_bufsize, et_bufsize, block_size)

    def set_score(self, score):
        self.score = score

    def __le__(self, other):
        return self.score < other.score

    def __ge__(self, other):
        return self.score > other.score

    def __lt__(self, other):
        return self.score <= other.score

    def __gt__(self, other):
        return self.score >= other.score

class Population():
    def __init__(self):
        self.repetition = int(os.getenv('REPETITION'))
        self.mutation = int(os.getenv('MUTATION'))
        self.crossover = int(os.getenv('CROSSOVER'))

        if self.repetition + self.mutation + self.crossover != 100:
            raise Exception

        self.pop_count = int(os.getenv('POP_CNT'))

        initial_compression_level = int(os.getenv('COMPRESSION_LEVEL'))
        initial_ce_bufsize = int(os.getenv('CE_BUFSIZE'))
        initial_et_bufsize = int(os.getenv('ET_BUFSIZE'))
        initial_block_size = int(os.getenv('BLOCKLEN'))
        initial_sample = Sample(
            initial_compression_level,
            initial_ce_bufsize,
            initial_et_bufsize,
            initial_block_size
        )
        self.samples = []

        self.__generate_initial__(initial_sample)
        

    def __generate_initial__(self, initial_sample):
        self.samples = [initial_sample]

        for _ in range(self.pop_count - 1):
            self.samples.append(initial_sample.mutate())

    def generate_next(self):
        self.samples.sort(reverse=True)

        new_samples = self.samples[0:3]

        for idx in range(3, self.pop_count):
            rand_num = random.randint(0, 99)

            if rand_num <= self.repetition:
                new_samples.append(new_samples[random.randint(0, idx - 1)])
            elif rand_num <= self.repetition + self.mutation:
                new_samples.append(new_samples[random.randint(0, idx - 1)].mutate())
            else:
                new_samples.append(new_samples[random.randint(0, idx - 1)].crossover(new_samples[random.randint(0, idx - 1)]))
