class A:
    def __init__(self):
        self.p = dict()
        self.p["1"] = 0.6
        self.p["0"] = 0.4


class B_A:
    def __init__(self):
        self.p = dict()
        self.p["11"] = 0.25
        self.p["10"] = 0.75
        self.p["01"] = 0.45
        self.p["00"] = 0.55


class C_A:
    def __init__(self):
        self.p = dict()
        self.p["11"] = 0.4
        self.p["10"] = 0.6
        self.p["01"] = 0.7
        self.p["00"] = 0.3


class D_BC:
    def __init__(self):
        self.p = dict()
        self.p["111"] = 0.8
        self.p["110"] = 0.2
        self.p["101"] = 0.7
        self.p["100"] = 0.3
        self.p["011"] = 0.6
        self.p["010"] = 0.4
        self.p["001"] = 0.5
        self.p["000"] = 0.5


class E_CD:
    def __init__(self):
        self.p = dict()
        self.p["111"] = 0.5
        self.p["110"] = 0.5
        self.p["101"] = 0.1
        self.p["100"] = 0.9
        self.p["011"] = 0.2
        self.p["010"] = 0.8
        self.p["001"] = 0.6
        self.p["000"] = 0.4


class F_D:
    def __init__(self):
        self.p = dict()
        self.p["11"] = 0.2
        self.p["10"] = 0.8
        self.p["01"] = 0.25
        self.p["00"] = 0.75


class G_DE:
    def __init__(self):
        self.p = dict()
        self.p["111"] = 0.5
        self.p["110"] = 0.5
        self.p["101"] = 0.3
        self.p["100"] = 0.7
        self.p["011"] = 0.5
        self.p["010"] = 0.5
        self.p["001"] = 0.7
        self.p["000"] = 0.3

