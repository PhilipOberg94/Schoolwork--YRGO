#pragma once

#include "vector.h"
#include "utils.h"

namespace ml
{

    class LinReg
    {
    public:
        LinReg(const double &bias, const double &weight,
               const container::Vector<double> &traininginput,
               const container::Vector<double> &trainingOutput,
               const double &learningRate);

        double getBias() const;
        double getWeight() const;
        int getTrainingSetCount() const;

        double predict(const double &input) const;
        void train(const int &epochs);

    private:
        double myBias;
        double myWeight;
        const double myLearningRate;
        const container::Vector<double> myTrainingInput;
        const container::Vector<double> myTrainingOutput;
    };

}
