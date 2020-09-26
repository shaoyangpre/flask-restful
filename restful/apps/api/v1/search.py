

def combinationSum2(int_list, k):
    result = []
    int_list.sort()
    res = [k, []]

    def backtrack(int_list, tmp, res):
        sum_res = sum(tmp)
        if abs(sum_res - k) < res[0]:
            res[0] = abs(sum_res - k)
            res[1] = tmp

        if sum_res > k:
            return
        if sum_res == k:
            result.append(tmp)
            return

        for i in range(len(int_list)):
            backtrack(int_list[i + 1:], tmp + [int_list[i]], res)
        return result

    final_result = backtrack(int_list, [], res)
    return res[1] if len(final_result) == 0 else final_result

if __name__ == "__main__":
    int_list = [1,2,3,4,5,6]
    k = 100
    print(combinationSum2(int_list, k))
