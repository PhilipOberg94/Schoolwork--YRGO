#pragma once

#include <vector>
#include <stdexcept>

namespace ml
{
    class LinReg
    {
    public:
        LinReg() = delete;

        LinReg(const std::vector<double> &myTrainingInput, const std::vector<double> &myTrainingOutput);

        const std::vector<double> &trainingInput() const;

        const std::vector<double> &trainingOutput() const;

        void train(std::size_t epochRun, double learningRate);

    private:
        std::vector<double> myTraningInput;
        std::vector<double> myTrainingOutput;
        double myWeight{};
        double myBias{};
    };

}