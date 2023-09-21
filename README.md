An attempt into face osint program. Uses Haar cascade to recognize a face, then reverse search service to find the information. Additionally saves results to .txt log and last search dump to .json file.

1. Run install.py to install required Python libraries
2. Get Copyseeker API here: https://rapidapi.com/Mano87/api/reverse-image-search-by-copyseeker/pricing. They have a free plan with 25 searches/month.
3. Find your API key and host in their API documentation and paste them to api_key.txt and host.txt
4. Make sure your target file path contains latin symbols only
5. Run face_seeker.py

Tested on Windows 10.
Requires Python3 and Copyseeker API subscription.
Regulate face recognition parameters in face_seeker.py if needed (marked by comments).

Special thanks to https://github.com/nokonoko for creating Uguu service
And to OpenCV developers
Btw, you can download some Haar cascades from here for customizing this thing: https://github.com/opencv/opencv/tree/4.x/data

Contact me if you meet any errors, I'll be thankful. And also contact me if you meet any better free reverse search API!

Support me: www.buymeacoffee.com/fairycorekvlt
