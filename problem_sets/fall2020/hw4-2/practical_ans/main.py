import numpy as np
import matplotlib.pyplot as plt
from distributions import A, B_A, C_A, D_BC, E_CD, F_D, G_DE

# get distribution of bayes net
A = A()
B_A = B_A()
C_A = C_A()
D_BC = D_BC()
E_CD = E_CD()
F_D = F_D()
G_DE = G_DE()


def get_p(variables):
    p_a = A.p[variables["A"]]
    p_b_a = B_A.p[variables["A"] + variables["B"]]
    p_c_a = C_A.p[variables["A"] + variables["C"]]
    p_d_bc = D_BC.p[variables["B"] + variables["C"] + variables["D"]]
    p_e_cd = E_CD.p[variables["C"] + variables["D"] + variables["E"]]
    p_f_d = F_D.p[variables["D"] + variables["F"]]
    p_g_de = G_DE.p[variables["D"] + variables["E"] + variables["G"]]
    return p_a * p_b_a * p_c_a * p_d_bc * p_e_cd * p_f_d * p_g_de


def get_p_condition(var, vars):
    vars[var] = "1"
    p1 = get_p(vars)
    vars[var] = "0"
    p0 = get_p(vars)
    p1_normal = p1 / (p1 + p0)
    p0_normal = 1 - p1_normal
    return p0_normal, p1_normal


def sample(vars, e_vars):
    for var in vars.keys():
        if var in e_vars.keys():
            continue
        p0, p1 = get_p_condition(var, vars)
        vars[var] = np.random.choice(["0", "1"], p=[p0, p1])


def initiate_sampler(evidence_vars):
    sampler = dict()
    sampler["A"] = np.random.choice(["0", "1"], p=[0.5, 0.5])
    sampler["B"] = np.random.choice(["0", "1"], p=[0.5, 0.5])
    sampler["C"] = np.random.choice(["0", "1"], p=[0.5, 0.5])
    sampler["D"] = np.random.choice(["0", "1"], p=[0.5, 0.5])
    sampler["E"] = np.random.choice(["0", "1"], p=[0.5, 0.5])
    sampler["F"] = np.random.choice(["0", "1"], p=[0.5, 0.5])
    sampler["G"] = np.random.choice(["0", "1"], p=[0.5, 0.5])
    for key in evidence_vars.keys():
        sampler[key] = evidence_vars[key]
    return sampler


if __name__ == '__main__':

    # sample input: A=1,B=0|C=1
    order = input().split("|")

    # set wanted variables
    wanted = dict()
    for w in order[0].split(","):
        wanted[w[0]] = w[-1]

    # set evidences
    evidences = dict()
    for ev in order[1].split(","):
        evidences[ev[0]] = ev[-1]

    # p(A=1,B=0|C=1) : 0.34615385
    exact_value = float(input())
    results = []
    repetion = []
    ave = 0
    for k in range(2, 21):
        vars = initiate_sampler(evidences)
        count = 0
        for i in range(k * 50):
            sample(vars, evidences)
            desired_sample = True
            for var in wanted.keys():
                if vars[var] != wanted[var]:
                    desired_sample = False
                    break

            if desired_sample:
                count += 1
        calculated = count / (k * 50)
        if k > 10:
            ave += calculated
        repetion.append(k * 50)
        result = 100 - (abs(exact_value - calculated) * 100) / exact_value
        # print(result)
        results.append(result)

    print(ave / 10)
    plt.scatter(repetion, results)
    plt.ylabel('percision %')
    plt.xlabel('repetion')
    plt.show()
