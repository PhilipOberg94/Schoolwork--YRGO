/*
 * lin_reg.cpp
 *
 * Created: 2024-09-18 10:20:44
 *  Author: Öberg
 */

#include "lin_reg.h"

namespace ml
{
    LinReg::LinReg(const double &bias, const double &weight, const container::Vector<double> &traininginput,
                   const container::Vector<double> &trainingOutput, const double &learningRate)

        : myBias(bias), myWeight(weight), myLearningRate(learningRate),
          myTrainingInput(traininginput), myTrainingOutput(trainingOutput)
    {
    }

    double LinReg::getBias() const
    {
        return myBias;
    }

    double LinReg::getWeight() const
    {
        return myWeight;
    }

    int LinReg::getTrainingSetCount() const
    {
        return myTrainingInput.size();
    }

    double LinReg::predict(const double &input) const
    {
        return myBias + myWeight * input;
    }

    void LinReg::train(const int &epochs)
    {

        for (int i = 0; i < epochs; i++)
        {
            const auto &reference{myTrainingOutput[i]};
            const auto &input{myTrainingInput[i]};
            if (input == 0)
            {
                myBias = reference;
            }
            else
            {
                for (auto j = 0U; j < myTrainingInput.size(); j++)
                {
                    double prediction = predict(myTrainingInput[j]);
                    double error = myTrainingOutput[j] - prediction;
                    myBias += error * myLearningRate;
                    myWeight += error * myLearningRate * input;
                }
            }
        }
    }
}
