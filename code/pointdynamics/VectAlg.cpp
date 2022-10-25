#include "VectAlg.h"

namespace alg {

	Vector3 operator*(const Vector3& v, float n) {
		return Vector3(v.x * n, v.y * n, v.z * n);
	}

	Vector3 operator-(const Vector3& v1, const Vector3& v2) {
		return Vector3(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z);
	}

	Vector3 operator+(const Vector3& v1, const Vector3& v2) {
		return Vector3(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z);
	}

	Vector2 operator*(const Vector2& v, float n) {
		return Vector2(v.x * n, v.y * n);
	}

	Vector3 operator*(const Matrix3x3& m, const Vector3& v) {

		float V[3]{ v.x,v.y,v.z };

		float ret[3]{ 0, 0, 0 };

		for (int row = 0; row < 3; row++)
			for (int col = 0; col < 3; col++) {

				ret[row] += m.m[row][col] * V[col];

			}


		return Vector3(ret[0], ret[1], ret[2]);

	}


	Matrix3x3 createTurnMatrix90(Vector3 v) {

		return Matrix3x3(v.x * v.x, v.x * v.y - v.z, v.x * v.z + v.y,
			v.y * v.x + v.z, v.y * v.y, v.y * v.z - v.x,
			v.z * v.x - v.y, v.z * v.y + v.x, v.z * v.z);

	}

	Vector2 showXY(Vector3 v) {
		return Vector2(v.x, v.y);
	}

	Vector2 showXZ(Vector3 v) {
		return Vector2(v.x, v.z);
	}

	Vector2 showYZ(Vector3 v) {
		return Vector2(v.y, v.z);
	}


	float abs(Vector3 v) {
		return sqrtf(v.x * v.x + v.y * v.y + v.z * v.z);
	}

	float abs(Vector2 v) {
		return sqrtf(v.x * v.x + v.y * v.y);
	}

	Vector3 getNormalized(Vector3 v) {
		return v * (1 / abs(v));
	}


}