#define NOMINMAX

#include <iostream>
#include <Windows.h>
#include <math.h>
#include <string.h>

#include <windows.h>

#include <SFML/Graphics.hpp>

#include "Src/Engine3D.h"
#include "Src/VectAlg.h"


void SetConsole(int px, int py, int w, int h) {

	HWND hWindowConsole = GetConsoleWindow(); 
	MoveWindow(hWindowConsole, px, py, w, h, TRUE);
}

namespace RotationTest {
	alg::Vector3 dragForce(alg::Vector3 r, alg::Vector3 v, float time) {

		alg::Vector3 ret;
		ret = v * (-1) * 0.99;

		return ret;
	}

	alg::Vector3 turn(alg::Vector3 r, alg::Vector3 v, float time) {
		if (alg::abs(v) != 0) {
			float absF = abs(v) * abs(v) / 500 * 1000;
			alg::Vector3 ret = createTurnMatrix90(alg::Vector3(5, -7, 10)) * alg::getNormalized(v);
			ret = ret * (1 / alg::abs(ret)) * -absF;
			return ret;
		}
		else return alg::Vector3(0, 0, 0);
	}

	void Test() {
		SetConsole(0, HEIGHT + 25, 800, 230);
		MaterialPoint mp(alg::Vector3(290.f, 320.f, 320.f), alg::Vector3(70, 0, 0), alg::Vector3(0, 0, 0));
		mp.addForce(dragForce);
		mp.addForce(turn);
		Engine engine(mp);
		engine.startEngine();
	}
}

namespace ForceFieldsTest {

	alg::Vector3 dragForce(alg::Vector3 r, alg::Vector3 v, float time) {

		alg::Vector3 ret;
		ret = v * (-1) * 0.9;

		return ret;
	}

#define CENTRAL_FORCE 200
#define SIDE_FORCE -400
#define VERTICAL_SIDE_FORCE -1200
#define VERTICAL_CENTRAL_FORCE -300
	alg::Vector3 SideField(alg::Vector3 r, alg::Vector3 v, float time) {

		if (r.z < 0.3 * HEIGHT)
			return alg::Vector3(0, 0, 0);

		if (!(r.x < 0.1 * WIDTH || r.y < 0.1 * WIDTH
			|| r.x > 0.9 * WIDTH || r.y > 0.9 * WIDTH)) {
			return alg::Vector3(0, 0, 0);
		}



		alg::Vector3 diff = alg::getNormalized(r - alg::Vector3(WIDTH / 2, WIDTH / 2, r.z));

		alg::Vector3 ret(SIDE_FORCE * diff.x, SIDE_FORCE * diff.y, VERTICAL_SIDE_FORCE);

		return ret;
	}

	alg::Vector3 LowField(alg::Vector3 r, alg::Vector3 v, float time) {

		if (r.z < 0.6 * HEIGHT)
			return alg::Vector3(0, 0, 0);

		alg::Vector3 diff = alg::getNormalized(r - alg::Vector3(WIDTH / 2, WIDTH / 2, r.z));

		alg::Vector3 ret(CENTRAL_FORCE * diff.x, CENTRAL_FORCE * diff.y, VERTICAL_CENTRAL_FORCE);

		return ret;
	}

	void Test() {
		SetConsole(0, HEIGHT + 25, 800, 230);
		MaterialPoint mp(alg::Vector3(290.f, 320.f, 320.f), alg::Vector3(0, 0, 0), alg::Vector3(0, 0, 0));
		mp.addForce(SideField);
		mp.addForce(LowField);
		mp.addForce(dragForce);
		mp.addForce(alg::Vector3(0, 0, 200));
		Engine engine(mp);
		engine.startEngine();
	}
}

namespace NonstationaryTest {
	alg::Vector3 dragForce(alg::Vector3 r, alg::Vector3 v, float time) {

		alg::Vector3 ret;
		ret = v * (-1) * 0.9;

		return ret;
	}

#define GRAVITY 350
#define Wt 1.5
#define At 0.3
#define Kx 0.3

	alg::Vector3 wave(alg::Vector3 r, alg::Vector3 v, float time) {

		float waveLevel = (0.6 + At * sin(Wt * time + Kx * r.x)) * HEIGHT;
		if (r.z < waveLevel)
			return alg::Vector3(0, 0, 0);

		alg::Vector3 ret(0, 0, -3 * GRAVITY);

		return ret;
	}

	void Test() {
		SetConsole(0, HEIGHT + 25, 800, 230);
		MaterialPoint mp(alg::Vector3(290.f, 320.f, 0.6 * HEIGHT - 30), alg::Vector3(20, -15, 0), alg::Vector3(0, 0, 0));
		mp.addForce(wave);
		mp.addForce(dragForce);
		mp.addForce(alg::Vector3(0, 0, GRAVITY));
		Engine engine(mp);
		engine.startEngine();
	}
}

namespace OscTest {
	alg::Vector3 dragForce(alg::Vector3 r, alg::Vector3 v, float time) {

		alg::Vector3 ret;
		ret = v * (-1) * 0.9;

		return ret;
	}


	alg::Vector3 force(alg::Vector3 r, alg::Vector3 v, float time) {

		auto dr = r - alg::Vector3(WIDTH / 2 + 60 * sin(time + 3.14 / 180 / 3), WIDTH / 2 + 30 * sin(time), WIDTH / 2);

		return dr * (-25);
	}



	void Test() {
		SetConsole(0, HEIGHT + 25, 800, 230);
		MaterialPoint mp(alg::Vector3(611.f, 320.f, 012.f), alg::Vector3(0, 0, 0), alg::Vector3(0, 0, 0));
		mp.addForce(dragForce);
		mp.addForce(force);
		Engine engine(mp);
		engine.startEngine();
	}
}

const std::string selectMessage = "Select test model:\n1 - 3D rotation\n2 - Force fields\n3 - Nonstationary waves\n4 - Oscillator";
const std::string errorMessage = "Invalid id\n";

int main()
{
START:

	SetConsole(300, 150, 540, 350);

	std::cout << selectMessage << std::endl;
	char id;
	std::cin >> id;

	switch (id) {
	case '1':
		RotationTest::Test();
		break;
	case '2':
		ForceFieldsTest::Test();
		break;
	case '3':
		NonstationaryTest::Test();
		break;
	case '4':
		OscTest::Test();
		break;

	default:
		system("cls");
		std::cout << errorMessage;
		goto START;
	}

	system("cls");
	goto START;

	return 0;
}