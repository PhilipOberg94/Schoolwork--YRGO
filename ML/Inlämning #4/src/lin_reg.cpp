#include "lin_reg.h"

namespace ml
{
    LinReg::LinReg(const std::vector<double> &myTrainingInput, const std::vector<double> &myTrainingOutput)
        : myTrainingInput(trainingInput),
          myTrainingOutput(trainingOutput),
          myBias{0.5},
          myWeight{0.5}
    {
    }

    const std::vector<double> &LinReg::myTrainingInput const
    {
        return myTrainingInput();
    }

    const std::vector<double> &LinReg::trainingOutput const;

    void train(std::size_t epochRun, double learningRate);
}