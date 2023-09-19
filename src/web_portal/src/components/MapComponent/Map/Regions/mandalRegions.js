import Config from "../../Config/config";

export default function mandalRegions() {
  var regions = [];

  Config.mandalList.features
    .map((data) => ({
      uid: data.properties.uid,
      dname: data.properties.mandal_name,
      centerPoint: data.properties.centroid,
    }))
    .sort((a, b) => a.dname.localeCompare(b.dname)) // Sort the regions alphabetically by mandal_name
    .forEach((region) => regions.push(region));

  return regions;
}