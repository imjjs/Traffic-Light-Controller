#ifndef CONTROLLOR_INTERSECTION2_HPP
#define CONTROLLOR_INTERSECTION2_HPP
#include <string>
#include <vector>
#include <map>
#include "Intersection.hpp"

class Intersection2 : public Intersection
{
private:
	std::vector<std::string> phaseCode;

protected:
	virtual void keepState() override;
	virtual void switchState() override;
	virtual void updateQLengthList() override;

public:
	Intersection2(std::string& _name): Intersection(_name) {};
	void loadPhaseCode(const std::map<std::string, std::vector<std::string>>&); 
	virtual ~Intersection2(){};
	void setThreshold(int, int);
	
};

#endif //CONTROLLOR_INTERSECTION2_HPP