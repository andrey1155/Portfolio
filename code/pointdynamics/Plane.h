#pragma once
#include "VectAlg.h"
#include <vector>
class Engine2D;
class Plane {
public:
	Plane(alg::Vector2,alg::Vector2,Engine2D*);
	void addForce(alg::Vector2);
	alg::Vector2 getPos(void) const;
	alg::Vector2 getV(void) const;
	void PhysicsUpdate(float);
	void addForceFunc(alg::Vector2(*)(alg::Vector2));
	std::vector<alg::Vector2> forces;
	std::vector<alg::Vector2(*)(alg::Vector2)> forcesFunc;
	alg::Vector2 v;
private:
	alg::Vector2 pos;

	alg::Vector2 a;
	const float mass = 100;
	Engine2D* engine;
};