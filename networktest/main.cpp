#include <fstream>
#include <string>
#include <iostream>
#include <regex>

int main()
{


    std::regex sensorPattern("^handleTrafficSensorInput.+?Sensor .(.+?)\tNumVehicles.(.+?)\tcontrollerID.(.+?)\tCurrentTime.(.+)");

    std::ifstream file("sumoInputForController.txt");
    std::string str;
    while (std::getline(file, str))
    {
        //std::cout<<str<<std::endl;

        std::string subject("Name: John Doe");
        std::string result;
          std::smatch match;
          if (std::regex_search(str, match, sensorPattern) && match.size() > 1) {
            result = match.str(1);
          } else {
            result = std::string("");
          }
          std::cout<<result<<std::endl;
    }
}
