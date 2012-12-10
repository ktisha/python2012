#include "prev.h"

#include <functional>
#include <memory>
#include <math.h>

typedef std::vector<std::vector<bool>*> dvec;

std::vector<std::vector<bool> > findPrev(std::vector<std::vector<bool> > t)
{
    std::function<int(std::vector<bool>)> vec2num = [&](std::vector<bool> v)
    {
        int res = 0;
        for (int i = 0; i < v.size(); i++)
        {
            res |= (v[i] << i);
        }
        return res;
    };

    std::vector<int> target(t.size());
    int h = target.size();
    int w = t[0].size();
    for (int i = 0; i < h; i++)
    {
        target[i] = vec2num(t[i]);
    }

    int count = powl(2, w);

    std::function<std::vector<bool>(int)> num2vec = [&](int num)
    {
        std::vector<bool> res = std::vector<bool>(w);
        for (int i = w - 1; i >= 0; i--)
        {
            res[i] = num % 2;
            num >>= 1;
        }
        return res;
    };

    std::function<bool(int, int, int, int)> checkCell = [&](int a, int b, int c, int pos)
    {
        std::function<bool(int , int)> get = [&](int n, int i)
        {
            i = (i + h) % h;
            return (n >> i) % 2;
        };

        int s = get(a, pos-1) + get(a, pos) + get(a, pos+1) +
                get(b, pos-1) +               get(b, pos+1) +
                get(c, pos-1) + get(c, pos) + get(c, pos+1);
        if (s == 3)
            return true;
        else if (s == 2)
            return get(b, pos);
        else
            return false;
    };

    std::vector<int> transitions(count * count * count);
    
    for (int i = 0; i < count; i++)
    {
        for (int j = 0; j < count; j++)
        {
            for (int k = 0; k < count; k++)
            {
                int res = 0;
                for (int l = 0; l < w; l++)
                {
                    res <<= 1;
                    res |= checkCell(i, j, k, l);
                }
                transitions[i * count * count + j * count + k] = res;
            }
        }
    }

    std::vector<std::vector<int>> newCands;

    for (int i = 0; i < count; i++)
    {
        for (int j = 0; j < count; j++)
        {
            for (int k = 0; k < count; k++)
            {
                if (transitions[i * count * count + j * count + k] == target[1])
                {
                    std::vector<int> cand(h);
                    cand[0] = i;
                    cand[1] = j;
                    cand[2] = k;
                    newCands.push_back(cand);
                }
            }
        }
    }

    for (int i = 3; i < h; i++)
    {
        std::vector<std::vector<int>> oldCands = std::move(newCands);
        newCands.clear();

        for (std::vector<int> j : oldCands)
        {
            for (int k = 0; k < count; k++)
            {
                std::vector<int> cand = j;
                cand[i] = k;
                if (transitions[cand[i-2] * count * count + cand[i-1] * count + cand[i]] == target[i-1])
                    newCands.push_back(cand);
            }
        }
    }

    std::vector<int> minCand;
    int minSum = w * h + 1;

    std::function<int(const std::vector<int>&)> onesCount = [](const std::vector<int>& v)
    {
        int res = 0;
        for (int num : v)
        {
            int i;
            for (i = 0; num; i++)
            {
                num &= num - 1;
            }
            res += i;
        }
        return res;
    };

    for (std::vector<int> cand : newCands)
    {
        if (transitions[cand[h-2] * count * count + cand[h-1] * count + cand[0]] == target[h-1] && 
            transitions[cand[h-1] * count * count + cand[0]   * count + cand[1]] == target[0])
        {
            int sum = onesCount(cand);
            if (sum < minSum)
            {
                minCand = cand;
                minSum = sum;
            }
        }
    }

    if (minSum <= w * h)
    {
        std::vector<std::vector<bool>> res(h);
        for (int i = 0; i < h; i++)
        {
            res[i] = num2vec(minCand[i]);
        }
        return res;
    }
    return std::vector<std::vector<bool>>(0);
}