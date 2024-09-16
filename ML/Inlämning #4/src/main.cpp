#include "lin_reg.h"

int main()
{
    const std::vector<double> input{0, 1};
    const std::vector<double> output{0, 1};
    ml::LinReg linReg{input, output};
}