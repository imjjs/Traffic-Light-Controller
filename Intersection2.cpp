#include "Intersection2.hpp"
#include "config.hpp"
void Intersection2::loadPhaseCode(const std::map<std::string, std::vector<std::string>>& dict)
{
	phaseCode = dict.at(name);
}

void Intersection2::setThreshold(int t1, int t2)
{
	for(auto& s : states)
	{
		s.threshold1 = t1;
		s.threshold2 = t2;
	}
}

void Intersection2::updateQLengthList()
{
	for(auto& s: sensors)
	{
		//PyObject *pValue = PyString_FromString(s);
		// Pyobject* pArgs = PyTuple_New(1);
		// PyTuple_SetItem(pArgs, 0, pValue);
		char* d = &s[0];
		PyObject *pResult = PyObject_CallMethod(pAreal, "getLastStepVehicleNumber","(s)", d);
		sensorToQlength[s] = PyInt_AsLong(pResult);
		//Py_DECREF(pValue);
		//Py_DECREF(pResult);
	}
	for( std::map<std::string, int>::const_iterator it = sensorToQlength.begin(); it != sensorToQlength.end(); ++it )
    {
      std::string key = it->first;
      int value = it->second;
	  std::cout<<"key, value:"<<key<<','<<value<<std::flush<<std::endl;
    }
}


void Intersection2::keepState()
{
	singleton.trafficlights.setRedYellowGreenState("tl" + name.substr(10) , phaseCode[currentStateIdx]);
}


void Intersection2::switchState()
{
	singleton.trafficlights.setRedYellowGreenState("tl" + name.substr(10) , phaseCode[currentStateIdx]);
	currentStateIdx = (currentStateIdx + 1) % states.size();
}
