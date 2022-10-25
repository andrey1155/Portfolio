/*

#include "Plane.h"
#include "Engine2D.h"
using namespace alg; 

Plane::Plane(alg::Vector2 pos, alg::Vector2 vel,Engine2D* engine) {
	this->pos = pos;
	this->v = vel;
	this->engine = engine;
}

void Plane::addForce(alg::Vector2 force) {
	forces.push_back(force);
	engine->addVector(force, this->pos);
}

void Plane::PhysicsUpdate(float dt) {
	alg::Vector2 R;
	for (int i = 0; i < forces.size() ; i++)
	{
		R = R + forces.at(i);
	}

	for (int i = 0; i < forcesFunc.size(); i++)
	{
		R = R + forcesFunc.at(i)(v);
	}
	a = R * (1 / mass);

	alg::Vector2 at = v * (1 / abs(v)/abs(v))*(v*a);
	alg::Vector2 an = a - at;
	//std::cout << abs(an) <<"    "<< abs(at)<<"   "<<abs(at+an)<<std::endl;
	alg::Vector2 newV = v + an*dt;
	alg::Vector2 deltha = newV - newV * (abs(v) / abs(newV));
	v = v + at * dt + (an-deltha)*dt;

	v = v + deltha * (-1);
	pos = pos + v * dt;
	std::cout << abs(v) << std::endl;
	//std::cout << abs(at) << std::endl;
}

alg::Vector2 Plane::getPos(void) const { return pos; }

alg::Vector2 Plane::getV(void) const { return v; }

void Plane::addForceFunc(alg::Vector2(*f)(alg::Vector2)){
	forcesFunc.push_back(f);
}

*/