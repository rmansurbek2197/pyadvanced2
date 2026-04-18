import re
from collections import defaultdict
from datetime import datetime

class LogPipeline:
    def __init__(self, filename):
        self.filename = filename

    def read_lines(self):
        with open(self.filename) as f:
            for line in f:
                yield line.strip()

    def filter_pattern(self, lines, pattern):
        regex = re.compile(pattern)
        for line in lines:
            if regex.search(line):
                yield line

    def parse(self, lines):
        for line in lines:
            parts = line.split()
            if len(parts) >= 3:
                user = parts[0]
                time = datetime.strptime(parts[1], "%H:%M:%S")
                yield user, time

    def sort(self, data):
        return sorted(data, key=lambda x: x[1])

    def stats(self, data):
        result = defaultdict(int)
        for user, _ in data:
            result[user] += 1
        for k, v in result.items():
            yield k, v

    def run(self, pattern):
        lines = self.read_lines()
        filtered = self.filter_pattern(lines, pattern)
        parsed = list(self.parse(filtered))
        sorted_data = self.sort(parsed)
        return self.stats(sorted_data)

pipeline = LogPipeline("log.txt")
for item in pipeline.run("ERROR"):
    print(item)
