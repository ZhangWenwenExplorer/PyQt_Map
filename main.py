import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QTimer, QUrl
import random

class RealTimeMapApp(QMainWindow):
    def __init__(self):
        super(RealTimeMapApp, self).__init__()
        self.setWindowTitle('实时地图轨迹')
        self.resize(800, 600)

        layout = QVBoxLayout()

        self.qwebengine = QWebEngineView(self)
        layout.addWidget(self.qwebengine)

        self.container = QWidget(self)
        self.container.setLayout(layout)
        self.setCentralWidget(self.container)

        self.qwebengine.setHtml(self.generate_map_html(), baseUrl=QUrl.fromLocalFile('.'))

        self.new_point = None
        self.old_point = None
        self.old_label = None  # 用于保存旧点的经纬度标签对象

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_map)
        self.timer.start(1000)  # 每秒更新一次地图

    def generate_map_html(self):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8" />
            <title>Real-time Map</title>
            <style>
                body, html, #map {
                    height: 100%;
                    margin: 0;
                }
            </style>
            <!-- 引入 Leaflet 的 CSS 和 JavaScript 文件 -->
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css">
            <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
        </head>
        <body>
            <div id="map" style="width: 100%; height: 100vh;"></div>
            <script>
                var mymap = L.map('map').setView([45.743215, 126.632628], 14);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '© OpenStreetMap contributors'
                }).addTo(mymap);
                var pathMarkers = L.layerGroup().addTo(mymap);

                var newMarkerIcon = L.icon({
                    iconUrl: 'C:/Users/22285/Desktop/test_python/leaflet/images/marker-icon.png',  // 用于新的轨迹点（注意修改路径）
                    iconSize: [16, 16],
                    iconAnchor: [8, 8]
                });

                var oldMarkerOptions = {
                    radius: 5,
                    fillColor: 'blue',
                    color: 'blue',
                    fillOpacity: 1
                };

                var oldMarker;  // 声明在外部以持久保存旧点的图标对象

                function addPoint(lat, lng, isNew) {
                    var latlng = new L.LatLng(lat, lng);
                    if (isNew) {
                        if (oldMarker) {
                            pathMarkers.removeLayer(oldMarker);  // 删除旧点的图标
                            mymap.removeLayer(oldLabel);  // 删除旧点的经纬度标签
                        }
                        oldMarker = L.marker(latlng, { icon: newMarkerIcon }).addTo(pathMarkers);
var label = L.divIcon({
  className: 'label',
  html: `<div style="white-space: nowrap; margin-left: 1em;">Lat: ${lat.toFixed(7)} Lng: ${lng.toFixed(7)}</div>`
});




                        var newLabel = L.marker(latlng, { icon: label }).addTo(pathMarkers);
                        oldLabel = newLabel;  // 保存旧点的经纬度标签对象
                    } else {
                        var marker = L.circleMarker(latlng, oldMarkerOptions).addTo(pathMarkers);
                    }
                    mymap.panTo(latlng);
                }
            </script>
        </body>
        </html>
        """
        return html

    def update_map(self):
        new_point = [45.743215 + random.uniform(-0.01, 0.01), 126.632628 + random.uniform(-0.01, 0.01)]
        if self.new_point is not None:
            self.old_point = self.new_point  # 保存上一个新点的坐标
        self.new_point = new_point

        # 使用 JavaScript 添加新的轨迹点到地图上x
        javascript = f"addPoint({new_point[0]}, {new_point[1]}, true);"
        self.qwebengine.page().runJavaScript(javascript)

        if self.old_point is not None:
            # 使用 JavaScript 添加旧的轨迹点到地图上，并连接成线
            lineCoordinates = "[[" + f"{self.old_point[0]},{self.old_point[1]}], [{new_point[0]},{new_point[1]}]]"
            javascript = f"var line = L.polyline({lineCoordinates}, {{color: 'red'}}).addTo(mymap);"
            self.qwebengine.page().runJavaScript(javascript)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = RealTimeMapApp()
    win.show()
    sys.exit(app.exec_())

