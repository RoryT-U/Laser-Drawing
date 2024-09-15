from svg.path import parse_path
from xml.dom import minidom


def get_point_at(path, distance, scale, offset):
    pos = path.point(distance)
    pos += offset
    pos *= scale
    return pos.real, pos.imag


def points_from_path(path, density, scale, offset):
    step = int(path.length() * density)
    last_step = step - 1

    if last_step == 0:
        yield get_point_at(path, 0, scale, offset)
        return

    for distance in range(step):
        yield get_point_at(
            path, distance / last_step, scale, offset)


def points_from_doc(doc, density=5, scale=1, offset=0):
    offset = offset[0] + offset[1] * 1j
    points = []
    for element in doc.getElementsByTagName("path"):
        for path in parse_path(element.getAttribute("d")):
            points.extend(points_from_path(
                path, density, scale, offset))

    return points


string = """
<svg version="1.0" xmlns="http://www.w3.org/2000/svg"
 width="1280.000000pt" height="911.000000pt" viewBox="0 0 1280.000000 911.000000"
 preserveAspectRatio="xMidYMid meet">
<g transform="translate(0.000000,911.000000) scale(0.100000,-0.100000)"
fill="#000000" stroke="none">
<path d="M0 0 l0 -660 210 0 210 0 0 245 0 245 163 0 c184 0 258 13 349
62 144 77 217 245 189 434 -21 143 -83 236 -192 286 -93 44 -137 48 -544 48
l-385 0 0 -660z m624 379 c49 -14 81 -46 97 -97 10 -35 9 -48 -5 -86 -27 -70
-67 -90 -193 -94 l-103 -4 0 146 0 146 83 0 c45 0 99 -5 121 -11z"/>
<path d="M6370 3480 l0 -660 205 0 205 0 2 268 3 267 44 -3 c53 -3 93 -23 119
-59 11 -16 73 -126 138 -246 64 -121 122 -221 128 -223 7 -2 111 -3 233 -2
l222 3 -110 211 c-119 229 -177 307 -256 348 l-45 22 44 13 c96 28 189 108
231 199 32 68 32 246 1 313 -30 64 -88 126 -148 156 -90 46 -166 52 -608 53
l-408 0 0 -660z m709 374 c74 -29 94 -134 37 -193 -35 -36 -102 -51 -232 -51
l-104 0 0 130 0 130 130 0 c95 0 140 -4 169 -16z"/>
<path d="M10700 3965 l0 -165 210 0 210 0 0 -495 0 -495 205 0 205 0 0 495 0
495 205 0 205 0 0 165 0 165 -620 0 -620 0 0 -165z"/>
<path d="M4150 1858 c0 -7 65 -303 144 -658 l143 -645 201 -3 201 -2 14 47 c8
27 59 209 113 405 61 221 102 352 106 343 5 -8 57 -188 117 -402 l109 -388
200 -3 c185 -2 201 -1 206 15 6 20 212 958 252 1143 13 63 26 125 29 138 l5
22 -193 0 -193 0 -37 -197 c-21 -109 -52 -271 -69 -361 -17 -90 -32 -161 -35
-159 -2 3 -48 164 -102 358 l-97 354 -195 3 -194 2 -79 -287 c-44 -159 -89
-322 -101 -363 -22 -74 -23 -74 -30 -40 -4 19 -35 181 -68 360 l-62 325 -193
3 c-150 2 -192 0 -192 -10z"/>
<path d="M183 1418 c3 -387 6 -451 22 -508 27 -99 71 -178 134 -241 106 -106
203 -137 446 -146 181 -6 287 8 382 52 74 33 190 151 226 227 54 114 57 146
57 621 l0 437 -205 0 -205 0 0 -437 c0 -404 -2 -441 -19 -478 -36 -78 -102
-115 -203 -115 -72 0 -129 23 -170 66 -52 56 -52 58 -56 527 l-3 437 -205 0
-206 0 5 -442z"/>
<path d="M2229 1783 c27 -75 72 -195 344 -913 l123 -325 221 -3 221 -2 10 27
c5 16 112 301 236 636 124 334 228 618 232 632 l6 25 -205 0 -206 0 -25 -82
c-173 -565 -262 -846 -267 -840 -6 6 -289 905 -289 917 0 3 -97 5 -215 5
l-215 0 29 -77z"/>
<path d="M9050 1856 c0 -2 115 -175 255 -384 l255 -380 0 -276 0 -276 205 0
205 0 0 276 0 276 245 365 c135 201 250 374 256 384 9 18 2 19 -215 19 l-225
0 -132 -220 c-73 -121 -134 -218 -137 -215 -3 3 -62 100 -132 217 l-127 213
-227 3 c-124 1 -226 0 -226 -2z"/>
<path d="M11090 1720 l0 -140 327 -2 328 -3 -368 -382 -368 -383 3 -132 3
-133 628 -3 628 -2 -3 142 -3 143 -376 5 -376 5 363 379 364 379 0 133 0 134
-575 0 -575 0 0 -140z"/>
<path d="M6910 1841 c0 -5 90 -147 200 -315 110 -168 200 -308 200 -311 0 -3
-101 -158 -225 -345 l-224 -340 229 0 228 0 125 202 c69 112 129 203 134 203
4 0 64 -91 132 -203 l124 -202 229 0 c181 0 228 3 222 13 -5 6 -104 158 -221
336 -118 179 -212 329 -210 335 3 6 91 145 197 310 105 164 194 305 197 312 4
12 -32 14 -215 14 l-221 0 -112 -201 c-61 -110 -115 -197 -120 -192 -5 5 -57
94 -117 198 l-110 190 -221 3 c-136 1 -221 -1 -221 -7z"/>
</g>
</svg>
"""

doc = minidom.parseString(string)
points = points_from_doc(doc, density=1, scale=10, offset=(0, 5))
doc.unlink()

import pygame
from svg.path import parse_path
from xml.dom import minidom

def main():
    screen = pygame.display.set_mode([500, 500])
    screen.fill((255, 255, 255))

    doc = minidom.parseString(string)
    points = points_from_doc(doc, 0.5, 1, (0, 5))
    doc.unlink()

    for point in points:
        pygame.draw.circle(screen, (0, 0, 255), point, 1)

    pygame.display.flip()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return


pygame.init()
main()
pygame.quit()