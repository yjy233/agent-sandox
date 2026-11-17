#include "helpers.hpp"

class Solution : public SolutionBase {
public:
    using SolutionBase::SolutionBase;
    int read(char* buf, int n) {
        // 调用 read4(buf4) 每次最多读 4 个字符
        throw std::runtime_error("TODO");
    }
};
