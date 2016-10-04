#include "Intersection.hpp"
#include "config.hpp"
#include "json.h"
#include <cassert>
#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <string>
#include <cassert>

std::map<std::string, std::string> Intersection::controllorIDTotrafficLightID;
static std::map<std::string, std::vector<std::string> > phaseCodes {
{"Controller202407913",{"GGGggGGGGgrrrr", "yyyggyyyygrrrr", "rrrGGrrrrGrrrr", "rrryyrrrryrrrr", "rrrrrrrrrrGGGG", "rrrrrrrrrryyyy"}},
{"Controller1443088096",{"GGGGggrrGGGGggrrrr", "yyyyggrryyyyggrrrr", "rrrrGGrrrrrrGGrrrr", "rrrryyrrrrrryyrrrr", "GrrrrrGGrrrrrrGGgg", "yrrrrryyrrrrrryygg", "rrrrrrrrrrrrrrrrGG", "rrrrrrrrrrrrrrrryy"}},
{"Controller202514078",{"GGGGggrrrrGGGGggrrrr", "yyyyggrrrryyyyggrrrr", "rrrrGGrrrrrrrrGGrrrr", "rrrryyrrrrrrrryyrrrr", "rrrrrrGGggrrrrrrGGgg", "rrrrrryyggrrrrrryygg", "rrrrrrrrGGrrrrrrrrGG", "rrrrrrrryyrrrrrrrryy"}},
{"Controller3010263944",{"GGggrrrrrGGggrrrrr", "yyggrrrrryyggrrrrr", "rrGGrrrrrrrGGrrrrr", "rryyrrrrrrryyrrrrr", "rrrrGGGggrrrrGGGgg", "rrrryyyggrrrryyygg", "rrrrrrrGGrrrrrrrGG", "rrrrrrryyrrrrrrryy"}},
{"Controller1443088101",{"GGGggrrrrGGGggrrrr", "yyyggrrrryyyggrrrr", "rrrGGrrrrrrrGGrrrr", "rrryyrrrrrrryyrrrr", "rrrrrGGggrrrrrGGgg", "rrrrryyggrrrrryygg", "rrrrrrrGGrrrrrrrGG", "rrrrrrryyrrrrrrryy"}}
};
class parseException {};

bool isYellowPhase(std::string controller, int idx)
{
	const auto& phases = phaseCodes.at(controller);
	std::string phase = phases[idx];
	if (phase.find('y')!=std::string::npos)
		return true;
	else
		return false;
}

void Intersection::debug(int a, int b)
{

	std::cout<<"current threshold:"<<states[0].threshold<<std::endl;
	std::cout<<"q1, q2:"<<a<<','<<b<<std::endl;
}

Intersection::Intersection(const std::string& _name) :name(_name), clock(0), currentStateIdx(0) {
}

void Intersection::loadFromJson(std::string& filename) {
	std::ifstream t(filename);
	std::string content((std::istreambuf_iterator<char>(t)),
		std::istreambuf_iterator<char>());

	Json::Value root;
	Json::Reader reader;
	//std::cout << "JSON filename: " << filename << std::endl;
	//std::cout << "JSON content: " << content << std::endl;
	//std::cout << "Calling parser" << std::endl;
	bool parsingSuccessful = reader.parse(content, root);
	//std::cout << "Parser finished" << std::endl;
	if (!parsingSuccessful) {
	    std::string parseErrorDetails = reader.getFormattedErrorMessages();
	  //  std::cout << "Error while parsing JSON: " << parseErrorDetails << std::endl;
		throw parseException();
	} else {
	    //std::cout << "Parsing was successful" << std::endl;
	}
	Json::Value controllor = root[name];
	Json::Value jsonStates = controllor["phases"];
	std::vector<std::string> phaseList;
	for (int i = 0; i < jsonStates.size(); ++i) {
		phaseList.push_back(jsonStates[i].asString());
	}
	int _minInterval, _maxInterval;
	int __minInterval = controllor["minInterval"].asInt();
	int __maxInterval = controllor["maxInterval"].asInt();
	int _threshold = controllor["threshold"].asInt();

	for (int i = 0; i < phaseList.size(); ++i) {
		std::string _phase = phaseList[i];
		//std::cout << "_phase = " << _phase << " and controller[PhaseToState][_phase] = " << controllor["PhaseToState"][_phase].asString() << std::endl << std::flush;
        Json::Value phase_desc = controllor["PhaseDescriptor"][_phase];
		std::string _state = phase_desc["flows"].asString();

        int _minInterval = phase_desc["minInterval"].asInt();
		int _maxInterval = phase_desc["maxInterval"].asInt();
		int _threshold = phase_desc["threshold"].asInt();

		if(true == isYellowPhase(name, i))
		{
		 	_minInterval = 50;
			_maxInterval = 50;
		}
		else
		{
			_minInterval = __minInterval;
			_maxInterval = __maxInterval;
		}

	//	std::cout << "Before adding state, no. of states: " << states.size() << std::endl << std::flush;
		State _s = { _state, _phase, _minInterval, _maxInterval, _threshold};
        std::cout <<_s.stateRow<<','<<_s.phase<<','<<_s.minInterval<<','<<_s.maxInterval<<','<<_s.threshold<<std::endl<<std::flush;
		states.push_back(_s);
      //  std::cout << "After adding state " << _state << ", no. of states: " << states.size() << std::endl << std::flush;
	}
	Json::Value _sensors = controllor["sensors"];
	for (int i = 0; i < _sensors.size(); ++i) {
		sensors.push_back(_sensors[i].asString());
		sensorToQlength[_sensors[i].asString()] = 0;
	}
}


void Intersection::setThreshold(int threshold, int phaseIdx)
{
	auto& s = states[phaseIdx];
	s.threshold = threshold;
}


void Intersection::updateQLength(std::string& sensor, int qLength) {
	sensorToQlength.at(sensor) = qLength;
}

void Intersection::calculateQLength(int* qLength1, int* qLength2) {
	assert(qLength1);
	assert(qLength2);
	*qLength1 = 0;
	*qLength2 = 0;
	const State state = states[currentStateIdx];
	const std::string& stateRow = state.stateRow;
	//std::cout<<"current stateRow:"<<stateRow<<std::flush<<std::endl;
	for (int i = 0; i < stateRow.length(); ++i) {
		if ('0' == stateRow[i]) {
			*qLength1 += sensorToQlength[sensors[i]];
		}
		else if ('1' == stateRow[i]) {
			*qLength2 += sensorToQlength[sensors[i]];
		}
		else {
			assert(false);
		}
	}
}

void Intersection::setStateByPhase(std::string phase) {
	int idx;
	bool stateFound = false;
	for (idx = 0; idx < states.size(); ++idx) {
		if (phase == states[idx].phase) {
		    stateFound = true;
			break;
		}
	}
	if(!stateFound) {
			assert(false);
	}
	currentStateIdx = idx;
	clock = 0;
}

bool Intersection::control() {
    //std::cout << "CurentStateIdx" << currentStateIdx << std::endl << std::flush;
    //std::cout << "No. of states = " << states.size() << std::endl << std::flush;
	State currentState = states[currentStateIdx];
	//std::cout << "C2" << std::flush << std::endl;
	//std::cout << "t1,t2: " << currentState.threshold1<<','<<currentState.threshold2<< std::endl;
	if (clock < currentState.minInterval)
		return false;

	if (clock >= currentState.maxInterval)
		return true;

	int q1, q2;
	//std::cout << "C3" << std::flush << std::endl;
	calculateQLength(&q1, &q2);
	//debug(q1,q2);
	//std::cout << "q1-q2: " <<q1<<','<<q2<<",threshold:"<<currentState.threshold<< std::endl;

	if (q1  - q2 > currentState.threshold)
	{
		//std::cout<<"q1 less eq than t1, keep state"<<std::endl;
		return true;
	}
	else
	{
		//std::cout<<"switch state"<<std::endl;
		return false;
	}
}

void Intersection::keepState() {}
void Intersection::switchState() {
    currentStateIdx = (currentStateIdx + 1) % states.size();
	for(auto& s: sensors){
		sensorToQlength.at(s) = 0;
	}
}

std::string Intersection::run() {
	updateQLengthList();
	if (true == control()) {
		switchState();
		clock = 0;
	}
	else {
		keepState();
		clock += 10;
	}
	return states[currentStateIdx].phase;
}

std::string Intersection::run(double _current_time) {
	assert(_current_time - currentTime > 0);
	updateQLengthList();
	if (true == control()) {
		switchState();
		clock = 0;
	}
	else {
		keepState();
		clock += (_current_time - currentTime)*10;
	}
	currentTime = _current_time;
	return states[currentStateIdx].phase;
}

void Intersection::print(){
	std::cout<<"intersection:"<< name<<std::endl;
	std::cout<<"currentIdx:"<<currentStateIdx<<std::endl;
	std::cout<<"clock:"<<clock<<std::endl;
	for(auto& s: sensors){
		std::cout<<"sensors-"<<s<<":"<<sensorToQlength.at(s)<<std::endl;
	}
}
