import React from "react";
import "../Common/common.css";
import Header from "../Common/Header";
import { BiX } from "react-icons/bi";
import { useHistory, Link } from "react-router-dom";
import { Row, Col, Button, Table } from "reactstrap";
import undplogo from "../img/undp-logo.png";
import telenganalogo from "../img/telengana-logo.png";
import telenganaagri from "../img/telengana-agri.png";
import icrisat from "../img/icrisat.png";
import jads from "../img/jads.png";
import rich from "../img/rich.jpg";
import rockefeller from "../img/rockefeller.png";
import tilburg from "../img/tilburg.png";
import misteo from "../img/MistEO_Logo_Square.png";
import { connect } from "react-redux";
import LoadingScreen from "react-loading-screen";
import logo from "../img/logo.png"
const mapStateToProps = (ReduxProps) => {
  return {
    Layers: ReduxProps.Layers,
  };
};
class Analytics extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
     loader : true
  }
}
componentDidMount() {
  this.page.addEventListener("load", this.handleIframeLoad); 
}
componentWillUnmount() {
  this.page.removeEventListener("load", this.handleIframeLoad)
}
handleIframeLoad = (event) => {
  this.setState({
    loader: false
  })
}
  render() {
    return (
      <React.Fragment>
        <div className="page-header">
          <Header />
        </div>
        <div className="about-body">
          <div>
            <Row style={{ paddingBottom: "10px" }}>
              <Col>
                <h6 className="page-heading">Site Analytics</h6>
              </Col>
              <Col>
                <Link to="/">
                  <BiX className="page-close" />
                </Link>
              </Col>
            </Row>
            <hr />
            <div>
              <div class="container analytics-page">
              <div class="iframe-container">
              <LoadingScreen
              loading={this.state.loader}
              bgColor="#f1f1f1"
              spinnerColor="#9ee5f8"
              textColor="#676767"
              logoSrc={logo}
              text="DiCRA"
              style={{ fontSize: "30px" }}
            >
              <iframe className="google-analytics" width="100%" height={2000} src="https://datastudio.google.com/embed/reporting/2aef4516-1c78-4a08-84d8-00eed13cd07b/page/1M" frameborder={0} style={{border:"0"}} allowfullscreen  ref={ frame => this.page = frame }></iframe>
              </LoadingScreen>
              </div>
              </div>
            </div>
          </div>
        </div>
      </React.Fragment>
    );
  }
}
export default connect(mapStateToProps)(Analytics);
