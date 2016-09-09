//
// Created by yli on 3/14/2016.
//

#ifndef CONTROLLOR_INTERSECTION_HPP
#define CONTROLLOR_INTERSECTION_HPP

#include <string>
#include <vector>
#include <map>



struct State {
	std::string stateRow;
	std::string phase;
	int minInterval;
	int maxInterval;
	int threshold1;
	int threshold2;
};


class Intersection {
protected:
	std::string name;
	std::vector<State> states;
	std::vector<std::string> sensors;
	std::map<std::string, int> sensorToQlength;
	int clock;

	void calculateQLength(int* qLength1, int* qLength2);
	virtual void keepState();
	virtual void switchState();
	virtual void updateQLengthList(){ };
public:
	int currentStateIdx;
	explicit Intersection() : name( "" ), clock( 0 ), currentStateIdx( 0 ) { };
	Intersection(const std::string& name);
	Intersection(const Intersection&) = delete;
	virtual ~Intersection() {};
	void loadFromJson(std::string& filename);
	void updateQLength(std::string& sensor, int qLength);
	void setStateByPhase(std::string phase);
	bool control();
	static std::map<std::string, std::string> controllorIDTotrafficLightID;
	std::string run();
	virtual void debug(int, int);
	void setThreshold(int, int);
	void print();
};


#endif //CONTROLLOR_INTERSECTION_HPP
