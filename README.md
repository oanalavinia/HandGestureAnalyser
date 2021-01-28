# Project FiiGezr
Gezr is a web application that has the purpose of creating a small structure out of Webcam-captured video-streams,
by detecting, classifying and comparing hand/ arm gestures of users, providing also information about rules resulted
from the input gesture. For this analysis, the data will be modeled using a Resource Description Framework (RDF) schema.
Simple users will conect to the application with camera on and they could see, by request, gestures data resulted until that point.
Also, an Admin user could get a JSON-LD with the analysed gestures statistics from all the conected users.  

## For production: SocketIO Streaming
We have a separate server implementation dedicated for production environments which uses socket streaming. It can be found on the `socket-streaming` branch.

### Project members
- Baisan Razvan
- Florean Oana-Lavinia
- Gafitescu Petru-Marian
