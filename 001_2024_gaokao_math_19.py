import copy


def get_ds_part(ds, i, m):
    if ds[i] >= m:
        mod = ds[i] % m
        s = ds[i] // m
        ds[i-1] = ds[i-1] + s
        ds[i] = mod
    return ds

def get_ds(k, m):
    ds = [0 for _ in range(m)]
    ds[-1] = ds[-1] + k
    for i in range(m-1, 0, -1):
        ds = get_ds_part(ds, i, m)
    for i in range(m):
        ds[i] = ds[i] + 1
    return ds


def deal_with_current_ds(arr, ds, m):
    # 分成m组，每组有4个元素
    groups = []
    # 检查每个组的元素是否在剩余元素中
    for gid in range(m):
        d = ds[gid]  # 当前组的公差
        group = []   # 当前组的元素
        a1 = arr[0]
        a2 = a1 + d
        a3 = a2 + d
        a4 = a3 + d
        if a1 in arr and a2 in arr and a3 in arr and a4 in arr:
            group = [a1, a2, a3, a4]
            arr.remove(a1)
            arr.remove(a2)
            arr.remove(a3)
            arr.remove(a4)
            groups.append(group)
        else:
            return False, groups
    return True, groups


def split(i, j, n, m):
    arr = [(k+1) for k in range(n)]
    # 删除2个元素
    arr.remove(i)
    arr.remove(j)

    mm = m ** m
    # 遍历所有的公差组合。如果所有的公差组合都不能满足条件，则数列不是(i, j)可分数列。
    # 如果至少有一个公差组合满足条件，则数列是(i, j)可分数列。
    for k in range(mm):
        # 每组的公差，可取[1, 1, ..., 1]或[1, 1, ..., 2]或...或[m, m, ..., m]。共有m^m种可能的取值。
        ds = get_ds(k, m)
        success, groups = deal_with_current_ds(copy.deepcopy(arr), ds, m)
        if success:
            return True, groups
    return False, []



if __name__ == "__main__":
    for m in range(1, 8):
        print('---------------------- m=%d ----------------------'%m)
        n = 4 * m + 2
        ij_count = 0
        for i in range(1, n, 1):
            for j in range(i+1, n+1, 1):
                success, groups = split(i, j, n, m)
                if success:
                    print('(i=%d, j=%d), groups=%s'%(i, j, groups))
                    ij_count += 1
        C_4mp2_2 = (2 * m + 1) * (4 * m + 1)
        P_m = ij_count / C_4mp2_2
        print('ij_count(1+m+m^2)=%d, C_4m+2^2=%d, Pm=%.4f > 0.125'%(ij_count, C_4mp2_2, P_m))
