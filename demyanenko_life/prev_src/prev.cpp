#include "prev.h"

#include <iostream>
#include <functional>
#include <memory>
#include <math.h>

using std::cout;
using std::endl;
typedef std::vector<std::vector<bool>*> dvec;

void printVec(const std::vector<bool>& v)
{
    for (bool i : v)
        cout << i;
    cout << endl;
}

std::vector<std::vector<bool> > findPrev(std::vector<std::vector<bool> > t)
{
    std::function<int(std::vector<bool>)> vec2num = [&](std::vector<bool> v)
    {
        int res = 0;
        for (int i = v.size() - 1; i >= 0; i--)
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
        for (int i = 0; i < w; i++)
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
        cout << "precalc i: " << i << endl;
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
        cout << "i: " << i << endl;
    }

    cout << "Checkpoint 1" << endl;

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

        cout << "Checkpoint " << i << endl;
    }

    cout << newCands.size() << endl;
    for (std::vector<int> cand : newCands)
    {
        if (transitions[cand[h-2] * count * count + cand[h-1] * count + cand[0]] == target[h-1] && 
            transitions[cand[h-1] * count * count + cand[0]   * count + cand[1]] == target[0])
        {
            std::vector<std::vector<bool>> res(h);
            for (int i = 0; i < h; i++)
            {
                res[i] = num2vec(cand[i]);
                printVec(res[i]);
            }
            cout << "test";
            cout << endl;
            return res;
        }
    }
    return std::vector<std::vector<bool>>(0);
}

void main()
{
    int size = 7;
    bool arr[] = {0, 0, 0, 0, 0, 0, 0,
                  0, 0, 1, 0, 0, 0, 0,
                  0, 0, 0, 1, 0, 0, 0,
                  0, 1, 1, 1, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0};

    std::vector<std::vector<bool> > field(size);
    for (int i = 0; i < size; i++)
    {
        field[i] = std::vector<bool>(size);
        for (int j = 0; j < size; j++)
        {
            field[i][j] = arr[i * size + j];
        }
    }

    std::vector<std::vector<bool> > prev = findPrev(field);
    cout << "Ya rodilsya!" << endl;
    for (int i = 0; i < size; i++)
    {
        for (int j = 0; j < size; j++)
        {
            cout << prev[i][j];
        }
        cout << endl;
    }
}