from math import inf


class MyTime:
    def __init__(self, hour, minute):
        self.hour = hour
        self.minute = minute

    def __gt__(self, other):
        if self.hour > other.hour:
            return True
        if self.hour == other.hour and self.minute > other.minute:
            return True
        return False


def have_overlap(interval_1, interval_2):
    if interval_1[1] > interval_2[0] and interval_2[1] > interval_1[0]:
        return True
    return False


def revise(c1, c2):
    if len(courses_profs[c2]) > 1:
        return False
    revised = False
    new_domain = []
    for prof in courses_profs[c1]:
        if len(courses_profs) != 0 and courses_profs[c2][0] != prof:
            new_domain.append(prof)
        else:
            revised = True
    courses_profs[c1] = new_domain
    return revised


def ac_3():
    queue = []
    for i in range(m):
        for j in arcs[i]:
            queue.append((i, j))
    while len(queue) != 0:
        c1, c2 = queue.pop()
        if revise(c1, c2):
            if len(courses_profs[c1]) == 0:
                return False
            for neighbor in arcs[c1]:
                if neighbor != c1:
                    queue.append((neighbor, c1))
    return True


def select_mrv(assignment):
    mrv = inf
    mrv_course = -1
    for course in range(len(assignment)):
        if assignment[course] == -1 and mrv > len(courses_profs[course]):
            mrv = len(courses_profs[course])
            mrv_course = course
    return mrv_course


def is_consistent(assignment, course, prof):
    for c in arcs[course]:
        if assignment[c] == prof:
            return False
    return True


def backtrack(assignment):
    ucourse = select_mrv(assignment)
    if ucourse == -1:
        return assignment
    for prof in courses_profs[ucourse]:
        if is_consistent(assignment, ucourse, prof):
            assignment[ucourse] = prof
            result = backtrack(assignment)
            if len(result) != 0:
                return result
            assignment[ucourse] = -1
    return []


def print_result(result):
    for i in result:
        print(i + 1)


m, n = map(int, input().split())
courses_profs = [[] for _ in range(m)]
courses_time = []
for _ in range(m):
    start, end = input().split("-")
    courses_time.append((
        MyTime(*map(int, start.split(":"))),
        MyTime(*map(int, end.split(":")))
    ))
for i in range(n):
    for course in map(int, input().split()):
        courses_profs[course - 1].append(i)

arcs = [[] for _ in range(m)]
for i in range(m):
    for j in range(m):
        if i != j and have_overlap(courses_time[i], courses_time[j]):
            arcs[i].append(j)


if ac_3():
    result = backtrack([-1 for i in range(m)])
    if len(result) != 0:
        print_result(result)
    else:
        print("NO")
else:
    print("NO")

# 5 3
# 8:00-9:00
# 8:30-9:30
# 9:00-10:00
# 9:00-10:00
# 9:30-10:30
# 3 4
# 2 3 4 5
# 1 2 3 4 5