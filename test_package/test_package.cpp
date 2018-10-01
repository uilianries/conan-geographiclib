#include <cstdlib>
#include <iostream>

#include <GeographicLib/Geodesic.hpp>

int main()
{
	const GeographicLib::Geodesic& geod = GeographicLib::Geodesic::WGS84();
    std::cout << "Bincrafters\n";
    return EXIT_SUCCESS;
}
