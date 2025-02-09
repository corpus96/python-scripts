import math

class NTC:
    def __init__(self, names):
        self.names = names
        self.init()

    def init(self):
        """
        Initialize the color names with their RGB and HSL values.
        """
        for i in range(len(self.names)):
            hex_color = f"#{self.names[i][0]}"
            rgb = self.rgb(hex_color)
            hsl = self.hsl(hex_color)
            self.names[i].extend([rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]])

    def name(self, color):
        """
        Find the closest named color to the given hex color.
        """
        color = color.upper()
        if len(color) < 3 or len(color) > 7:
            return ["#000000", f"Invalid Color: {color}", False]

        # Convert shorthand hex to full hex if needed (e.g., #123 -> #112233)
        if len(color) == 4:
            color = f"#{color[1]*2}{color[2]*2}{color[3]*2}"

        rgb = self.rgb(color)
        hsl = self.hsl(color)

        r, g, b = rgb
        h, s, l = hsl
        cl = -1
        df = -1

        for i in range(len(self.names)):
            # Check for an exact match
            if color == f"#{self.names[i][0]}":
                return [f"#{self.names[i][0]}", self.names[i][1], True]

            # Calculate distance in RGB and HSL spaces
            ndf1 = (r - self.names[i][2])**2 + (g - self.names[i][3])**2 + (b - self.names[i][4])**2
            ndf2 = (h - self.names[i][5])**2 + (s - self.names[i][6])**2 + (l - self.names[i][7])**2
            ndf = ndf1 + ndf2 * 2

            if df < 0 or df > ndf:
                df = ndf
                cl = i

        if cl < 0:
            return ["#000000", f"Invalid Color: {color}", False]

        return [f"#{self.names[cl][0]}", self.names[cl][1], False]

    def rgb(self, color):
        """
        Convert a hex color to RGB.
        """
        return [
            int(color[1:3], 16),
            int(color[3:5], 16),
            int(color[5:7], 16)
        ]

    def hsl(self, color):
        """
        Convert a hex color to HSL.
        """
        r, g, b = [int(color[1:3], 16) / 255, int(color[3:5], 16) / 255, int(color[5:7], 16) / 255]
        min_val = min(r, g, b)
        max_val = max(r, g, b)
        delta = max_val - min_val

        #Calculate lightness
        l = (min_val + max_val) / 2

        #Calculate the saturation
        s = 0
        if l > 0 and l < 1:
            s = delta / (2 * l if l < 0.5 else 2 - 2 * l)

        #Calculate hue
        h = 0
        if delta > 0:
            if max_val == r and max_val != g:
                h += (g - b) / delta
            if max_val == g and max_val != b:
                h += 2 + (b - r) / delta
            if max_val == b and max_val != r:
                h += 4 + (r - g) / delta
            h /= 6

        return [int(h * 255), int(s * 255), int(l * 255)]