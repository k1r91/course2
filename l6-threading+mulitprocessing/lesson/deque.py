from collections import deque

d = deque()
d.append(12)
d.append(14)
print(d)
d.appendleft(155)
print(d)
c = d.pop()
print(d, c)
e = d.popleft()
print(d, e)
d1 = deque(maxlen=2)
d1.append(2)
d1.append(3)
print(d1)
d1.append(4)
d1.append(5)
print(d1)