using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using System.Net.Http;
using Newtonsoft.Json;
using MongoDB.Driver;
using MongoDB.Bson;
using CloudinaryDotNet;
using CloudinaryDotNet.Actions;
using System.Net;

namespace ahj.Controllers
{
    public class HomeController : Controller
    {
        public class AdditionalInformation
        {
            public string age { get; set; }
        }

        public class Face
        {
            public int left { get; set; }
            public int top { get; set; }
            public int width { get; set; }
            public int height { get; set; }
            public AdditionalInformation additional_information { get; set; }
        }

        public class HpeFace
        {
            public List<Face> face { get; set; }
        }
        public class FaceImg
        {
            public string url { get; set; }
        }
        public class HpeRef
        {
            public string reference { get; set; }
        }

        public class FaceRectangle
        {
            public int top { get; set; }
            public int left { get; set; }
            public int width { get; set; }
            public int height { get; set; }
        }

        public class HeadPose
        {
            public double pitch { get; set; }
            public double roll { get; set; }
            public double yaw { get; set; }
        }

        public class FacialHair
        {
            public double moustache { get; set; }
            public double beard { get; set; }
            public double sideburns { get; set; }
        }

        public class FaceAttributes
        {
            public double smile { get; set; }
            public HeadPose headPose { get; set; }
            public string gender { get; set; }
            public double age { get; set; }
            public FacialHair facialHair { get; set; }
            public string glasses { get; set; }
        }

        public class FaceData
        {
            public string faceId { get; set; }
            public FaceRectangle faceRectangle { get; set; }
            public FaceAttributes faceAttributes { get; set; }
        }
        public async Task<JsonResult> Index()
        {
            string imgurl = this.Request.Query["url"];
            if (imgurl != null)
            {
                try {
                    HttpClient h = new HttpClient();
                        // h.BaseAddress =new Uri("https://api.projectoxford.ai/face/v1.0/detect?returnFaceId=true&returnFaceLandmarks=false&returnFaceAttributes=age,gender,smile,glasses,facialHair");
                        h.DefaultRequestHeaders.TryAddWithoutValidation("Ocp-Apim-Subscription-Key", "7f7851370b27432c8721fda709076e86");
                    Account account = new Account(
                                  "angelhackjaipur",
                                  "316152125247843",
                                  "ajrPDyhdVkcHZvpoPZeTv15PhPc");
                    WebClient webClient = new WebClient();
                    webClient.DownloadFile(imgurl, "test.jpg");
                    Cloudinary cloudinary = new Cloudinary(account);
                    var uploadParams = new ImageUploadParams()
                    {
                        File = new FileDescription(@"test.jpg")
                    };
                    var uploadResult = cloudinary.Upload(uploadParams);
                    FaceImg f = new FaceImg { url = uploadResult.Uri.AbsoluteUri};
                    var d = await h.PostAsync("https://api.projectoxford.ai/face/v1.0/detect?returnFaceId=true&returnFaceLandmarks=false&returnFaceAttributes=age,gender,smile,glasses,facialHair,headPose", new StringContent(JsonConvert.SerializeObject(f), System.Text.Encoding.UTF8, "application/json"));
                    string rawdata = await d.Content.ReadAsStringAsync();
                    List<FaceData> faceData = JsonConvert.DeserializeObject<List<FaceData>>(rawdata);
                        var face = faceData[0];
                    var client = new MongoClient("mongodb://172.16.22.196:27017");
                    var database = client.GetDatabase("ahj");
                    var collection = database.GetCollection<BsonDocument>("facedata");
                    var document = new BsonDocument {
                        { "faceId", face.faceId},
                        { "faceRectangle", new BsonDocument {
                            {"top",face.faceRectangle.top },
                            {"left",face.faceRectangle.left },
                            {"width",face.faceRectangle.width },
                            {"height",face.faceRectangle.height }
                        } },
                        { "faceAttributes", new BsonDocument {
                            {"smile",face.faceAttributes.smile },
                            {"glasses",face.faceAttributes.glasses },
                            {"headPose",new BsonDocument {
                                {"pitch",face.faceAttributes.headPose.pitch },
                                {"roll",face.faceAttributes.headPose.roll },
                                {"yaw",face.faceAttributes.headPose.yaw }
                            } },
                            {"gender",face.faceAttributes.gender },
                            {"age",face.faceAttributes.age },
                            {"facialHair",new BsonDocument {
                                {"moustache",face.faceAttributes.facialHair.moustache },
                                {"beard",face.faceAttributes.facialHair.beard },
                                {"sideburns",face.faceAttributes.facialHair.sideburns },
                            } },
                        } },
                    };
                        await collection.InsertOneAsync(document);
                    HttpResponseMessage hpe=await h.PostAsync("https://api.havenondemand.com/1/api/sync/storeobject/v1?url="+f.url+"&apikey=54f20327-b690-4cd1-9494-06e044b88e2c", new StringContent("", System.Text.Encoding.UTF8, "application/json"));
                    string hperef=await hpe.Content.ReadAsStringAsync();
                    HpeRef href = JsonConvert.DeserializeObject<HpeRef>(hperef);
                    hpe = await h.PostAsync("https://api.havenondemand.com/1/api/sync/detectfaces/v1?reference="+href.reference+"&additional=true&apikey=54f20327-b690-4cd1-9494-06e044b88e2c", new StringContent("", System.Text.Encoding.UTF8, "application/json"));
                    hperef = await hpe.Content.ReadAsStringAsync();
                    HpeFace hpeface = JsonConvert.DeserializeObject<HpeFace>(hperef);
                    var hpeFaceBsonObject = hpeface.ToBsonDocument();
                    await collection.InsertOneAsync(hpeFaceBsonObject);
                    JsonResult j = new JsonResult("Ok");
                    return j;
             }
                catch(Exception e) {
                    JsonResult jjj = new JsonResult("url galat hai" + e.Message.ToString());
                    return jjj;
                }
            }
            JsonResult jj = new JsonResult("url khaali hai");
            return jj;
        }
    }
}
