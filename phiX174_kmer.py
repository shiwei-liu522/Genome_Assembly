#Python3

import sys

class S_Recon:
    def __init__(self):
        self.k, self.adj = self.readData()
        # self.path = EulerianPath(self.adj).calculateEulerianPath()
        self.path = EulerianPath(self.adj).ECycle()
        print(self.re_path(self.path)[:-self.k + 1])

    def readData(self):
        data = list(sys.stdin.read().strip().split())
        adj = self.deBrujin(len(data[0]), data)
        return len(data[0]), adj

    def deBrujin(self, k, patterns):
        adjdb = dict()
        for p in patterns:
            if p[:k - 1] in adjdb:
                adjdb[p[:k - 1]].append(p[1:])
            else:
                adjdb[p[:k - 1]] = []
                adjdb[p[:k - 1]].append(p[1:])
            if p[1:] not in adjdb:
                adjdb[p[1:]] = []
        return adjdb

    def re_path(self, path):
        return path[0] + ''.join(seq[-1] for seq in path[1:])

class EulerianPath:
    def __init__(self, adj):
        self.adj = adj
        self.update()

    def _input(self):
        data = list(sys.stdin.read().strip().split())
        curMax = 0
        for i in range(len(data) // 3):
            curMax = max(int(data[i * 3]), curMax, max(list(map(int, data[i * 3 + 2].split(',')))))
        self.n = curMax + 1
        self.adj = [[]] * self.n
        self.unusedEdges = [[]] * self.n
        self.inDeg = [0] * self.n
        self.outDeg = [0] * self.n
        self.adjCurPos = [0] * self.n
        for i in range(len(data) // 3):
            curIn = int(data[i * 3])
            self.adj[curIn] = list(map(int, data[i * 3 + 2].split(',')))
            for v in self.adj[curIn]:
                self.inDeg[v] += 1
            l = len(self.adj[curIn])
            self.outDeg[curIn] = l
            self.unusedEdges += l

    def update(self):
        self.n = len(self.adj)
        self.unusedEdges = 0
        self.nodesWUE,self.inDeg,self.outDeg,self.adjCurPos = dict(), dict(), dict(), dict()
        self.path = []
        self.unbalanced = []
        for w, vList in self.adj.items():
            self.inDeg[w] = self.inDeg.get(w, 0)
            for v in vList:
                self.inDeg[v] = self.inDeg.get(v, 0) + 1
            l = len(vList)
            self.outDeg[w] = l
            self.unusedEdges += l
            self.adjCurPos[w] = 0

    def add(self):
        if type(self.adj) is dict:
            for v in self.adj.keys():
                if self.inDeg[v] != self.outDeg[v]:
                    if self.inDeg[v] < self.outDeg[v]:
                        self.unbalanced.append(v)
                    else:
                        self.unbalanced.insert(0, v)
            if len(self.unbalanced) > 0:
                self.adj[self.unbalanced[0]].append(self.unbalanced[1])
                self.outDeg[self.unbalanced[0]] += 1
                self.inDeg[self.unbalanced[1]] += 1
            return
        for v in range(self.n):
            if self.inDeg[v] != self.outDeg[v]:
                if self.inDeg[v] < self.outDeg[v]:
                    self.unbalanced.append(v)
                else:
                    self.unbalanced.insert(0, v)
        if len(self.unbalanced) > 0:
            self.adj[self.unbalanced[0]].append(self.unbalanced[1])
            self.outDeg[self.unbalanced[0]] += 1
            self.inDeg[self.unbalanced[1]] += 1
        return

    def view(self, s):
        self.path.append(s)
        curPos = self.adjCurPos[s]
        curMaxPos = self.outDeg[s]
        while curPos < curMaxPos:
            self.adjCurPos[s] = curPos + 1
            if curPos + 1 < curMaxPos:
                self.nodesWUE[s] = len(self.path) - 1
            else:
                if s in self.nodesWUE:
                    del self.nodesWUE[s]
            v = self.adj[s][curPos]
            self.path.append(v)
            s = v
            curPos = self.adjCurPos[s]
            curMaxPos = self.outDeg[s]
            self.unusedEdges -= 1
        return

    def updatePath(self, startPos):
        l = len(self.path) - 1
        self.path = self.path[startPos:l] + self.path[:startPos]
        for node, pos in self.nodesWUE.items():
            if pos < startPos:
                self.nodesWUE[node] = pos + l - startPos
            else:
                self.nodesWUE[node] = pos - startPos
        return

    def ECycle(self):
        if type(self.adj) is dict:
            w, vList = self.adj.popitem()
            self.adj[w] = vList
            self.view(w)
        else:
            self.view(0)
        while self.unusedEdges > 0:
            node, pos = self.nodesWUE.popitem()
            self.updatePath(pos)
            self.view(node)
        return self.path

    def EPath(self):
        self.add()
        self.ECycle()
        if len(self.unbalanced) > 0:
            for i in range(len(self.path) - 1):
                if self.path[i] == self.unbalanced[0] and self.path[i + 1] == self.unbalanced[1]:
                    self.updatePath(i + 1)
                    break
        return self.path

    def printPath(self):
        print('->'.join([str(node) for node in self.path]))

    def saveResult(self):
        f = open('result.txt', 'w')
        f.write('->'.join([str(node) for node in self.path]))


if __name__ == "__main__":
    S_Recon()