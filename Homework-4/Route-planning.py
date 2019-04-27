# generate data
import random
import matplotlib.pylab as plt
import time

random.seed(1)
latitude = [random.randint(-100, 100) for _ in range(20)]
longtitude = [random.randint(-100, 100) for _ in range(20)]
points = list(zip(latitude, longtitude))

# plot
plt.scatter(latitude, longtitude)


# build graph: represent graph in a adjacent matrix
import sys
class Solution:
    def shortestRoute(self, points, P):
        # build graph
        # memorize state : and corresponding optimal pair of route and cost
        global memo
        self.memo = [{} for i in range(len(points)+1)]
        memo = self.memo
        points = [P] + points
        return self.dfs(points, 1, 0)[0][::-1]

    def dfs(self, points, state, currpoint):
        if state + 1 == (1 << len(points)):
            return [[currpoint], 0]

        if state in self.memo[currpoint]:
            return self.memo[currpoint][state]

        minimum = sys.maxsize
        for i in range(len(points)):
            if state & (1 << i) > 0:
                continue
            route, distance = self.dfs(points, state + (1 << i), i)
            tmp_distance = distance + self.distance(points[currpoint], points[i])
            if tmp_distance < minimum:
                minimum = tmp_distance
                self.memo[currpoint][state] = (route + [currpoint], tmp_distance)
        return self.memo[currpoint][state]

    def distance(self, p1, p2):
        return sum(map(lambda x: (x[0] - x[1]) ** 2, zip(p1, p2))) ** (1/2)


class Solution2:
    def shortestRoute(self, points, P):
        memo = [{} for i in range(len(points) + 1)]
        points = [P] + points
        queue = [([0], 0, 1)]

        minimum = sys.maxsize
        minicase = []
        while queue:
            # print(queue)
            curr_length = len(queue)
            while curr_length > 0:
                curr_length -= 1
                route, distance, state = queue.pop(0)
                currpoint = route[-1]
                if state + 1 == 1 << len(points):
                    if distance < minimum:
                        minimum = distance
                        minicase = route
                    continue
                if state in memo[currpoint] and memo[currpoint][state] < distance:
                    continue
                memo[currpoint][state] = distance
                for i in range(len(points)):
                    if state & (1 << i) > 0:
                        continue
                    tmp_distance = distance + self.distance(points[currpoint], points[i])
                    queue.append((route + [i], tmp_distance, state + (1 << i)))
        return minicase

    def distance(self, p1, p2):
        return sum(map(lambda x: (x[0] - x[1]) ** 2, zip(p1, p2))) ** (1 / 2)


if __name__ == '__main__':
    st = time.clock()
    print(Solution().shortestRoute(points, (5, 10))[0][::-1])
    st2 = time.clock()
    print("time1: ", st2 - st)
    # print(Solution2().shortestRoute(points, (5, 10)))
    # print("time2: ", time.clock() - st2)