using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LambdaManBoardUtil
{
    [JsonObject]
    public class BoardFrame
    {
        [JsonProperty("tick")]
        public uint TickNumber { get; set; }

        [JsonProperty("board")]
        public byte[][] Board { get; set; }

        public List<Ghost>

        public BoardFrame()
        {

        }

        public BoardFrame(uint tickNumber, byte[][] board)
        {
            TickNumber = tickNumber;
            Board = board;
        }
    }

    [JsonObject]
    public class Ghost
    {
        [JsonProperty("direction")]
        public int Direction { get; set; }

        [JsonProperty("location")]
        [JsonConverter(typeof(LocationConverter))]
        public Location Location { get; set; }
    }

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

            writer.WriteValue(new List<int>() { location.X, location.Y });
        }

        public override object ReadJson(JsonReader reader, Type objectType, object existingValue, JsonSerializer serializer)
        {
            Console.WriteLine(reader.Value);
            //JArray a = JArray.Parse(reader.Value);
            //var location = new Location()

            return null;
        }
    }
}
