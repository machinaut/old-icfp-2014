using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LambdaManBoardUtil
{
    [Serializable]
    [JsonObject]
    public class BoardFrame
    {
        [JsonProperty("tick")]
        public uint TickNumber { get; set; }

        [JsonProperty("board")]
        public byte[][] Board { get; set; }

        [JsonProperty("ghosts")]
        public List<Ghost> Ghosts { get; set; }

        [JsonProperty("lambdaMan")]
        public LambdaMan LambdaMan { get; set; }

        public BoardFrame()
        {

        }

        public BoardFrame(uint tickNumber, byte[][] board)
        {
            TickNumber = tickNumber;
            Board = board;
        }
    }

    [Serializable]
    [JsonObject]
    public class Ghost
    {
        [JsonProperty("direction")]
        public int Direction { get; set; }

        [JsonProperty("location")]
        [JsonConverter(typeof(LocationConverter))]
        public Location Location { get; set; }
    }

    [Serializable]
    public class LambdaMan
    {
        [JsonProperty("direction")]
        public int Direction { get; set; }

        [JsonProperty("score")]
        public int Score { get; set; }

        [JsonProperty("lives")]
        public int Lives { get; set; }

        [JsonProperty("location")]
        [JsonConverter(typeof(LocationConverter))]
        public Location Location { get; set; }

        [JsonProperty("vitality")]
        public int Vitality { get; set; }
    }

    [Serializable]
    [JsonObject]
    public class Location
    {
        public int X { get; set; }

        public int Y { get; set; }

        public Location(int x, int y)
        {
            X = x;
            Y = y;
        }
    }

    public class LocationConverter : JsonConverter
    {
        public override void WriteJson(JsonWriter writer, object value, JsonSerializer serializer)
        {
            var location = value as Location;
            writer.WriteStartArray();
            //writer.WriteValue(new List<int>() { location.X, location.Y });
            writer.WriteValue(location.X);
            writer.WriteValue(location.Y);
            writer.WriteEndArray();
        }

        public override object ReadJson(JsonReader reader, Type objectType, object existingValue, JsonSerializer serializer)
        {
            JArray jObject = JArray.Load(reader);
            var x = (int)JsonConvert.DeserializeObject(jObject.First.ToString(), typeof(int));
            var y = (int)JsonConvert.DeserializeObject(jObject.Last.ToString(), typeof(int));
            return new Location(x, y);
        }

        public override bool CanConvert(Type objectType)
        {
            //return (objectType == typeof(Location));
            return true;
        }
    }
}
