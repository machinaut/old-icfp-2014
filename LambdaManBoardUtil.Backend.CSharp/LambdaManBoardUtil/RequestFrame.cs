using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LambdaManBoardUtil
{
    [JsonObject]
    public class MessageFrame
    {
        [JsonProperty("type")]
        public string Type { get; set; }

        [JsonProperty("params")]
        public string Parameters { get; set; }
    }

}
